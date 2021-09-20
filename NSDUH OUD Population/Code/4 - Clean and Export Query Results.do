/*****************************************
* DRAFT - PRIVILEGED AND CONFIDENTIAL 
* Project:    6800
* Analyst:    KM
* Date:       4 May 2020
* Purpose:    Create Use NBER TAXSIM Tool
* Audited:    N
*****************************************/

cd "C:/Users/Karna Malaviya/Desktop/OUD/" 


************************************************************
*   Prepare National Estimates for Merge with State Data   *	
************************************************************

	import delimited "Output\national_oud_pop 2020-06-16", clear
	
	rename population national_avg_oud_pop
	drop wt_var url
	
	tempfile national
	save `national', replace
	
	
*******************************
*   Clean and Export Output   *	
*******************************

	import delimited "Output\state_oud_pop 2020-06-16", clear
	
	* 1 - Merge in National Estimates
	merge m:1 year_start year_end variable control using `national', nogen
	
	* 2 - To Find OUD, Keep Pain Killer ONLY and Heroin in pre-2015 Period
	drop if variable == "ABODANL" & control == "NONE"
	
	* 2 - Adjust Suppressed Values With National Estimate
		* 2.1 - Destring Values, Keeping Suppressed as Missing
		foreach var of varlist population national_avg_oud_pop {
			gen `var'_num = `var'
			destring `var'_num, ignore(",Suppressed") replace
			}	
	
		* 2.2 - Find Difference Between National OUD Pop and Sum Over Non-Suppressed States
		bysort query (stname) : egen state_sum_notsuppressed = total(population_num)
		gen total_suppressed = national_avg_oud_pop_num - state_sum_notsuppressed
		tab total_suppressed
		replace total_suppressed = 0 if total_suppressed < 0
		
		* 2.3 - Suppressed Imputation is Total Suppressed Divived by Count Number of Suppressed States In Query
		gen temp = cond(population == "Suppressed", 1, 0)
		bysort query year_* variable control (stname) : egen states_suppressed = total(temp)
		gen suppression_impuation = total_suppressed / states_suppressed
		drop temp
		
		* 2.4 - Assign Suppressed Values
		gen population_clean = cond(population == "Suppressed", suppression_impuation, population_num)
		
	* 3 - Reshape Wide
	drop url query population_num control wt_var national_avg_oud_pop* *suppress*
	reshape wide population*, i(stname year_*) j(variable) string
	rename population* *_str
	rename _clean*_str *
	rename *, lower
	order *_str, last
				
	* 4 - OUD Population Variable
	egen temp_oud = rowtotal(abodanl abodher)
	gen avg_oud_pop = cond(!mi(udpyopi), udpyopi, temp_oud)
	
	* 5 - Reshape Wide to State Level
	tostring year_*, replace
	gen year = year_start + "_" + year_end
	keep stname year avg_oud_pop
	rename avg_oud_pop avg_oud_pop_
	reshape wide avg_oud_pop_, i(stname) j(year) string
	
	* 6 - Convert Data to Annual
	drop avg_oud_pop_2014_2015
		* 6.1 - For All Years Except 2014, Use Average Covered by Year
		* If 2 averages cover the year (2016 and 2017), use the average of the 2 averages
		forv year = 2002 / 2018 {
			local year_lead = `year' + 1
			local year_lag = `year' - 1
			
			gen oud_pop_`year' = .
			capture replace oud_pop_`year' = avg_oud_pop_`year_lag'_`year' ///
											 if !mi(avg_oud_pop_`year_lag'_`year')
			capture replace oud_pop_`year' = avg_oud_pop_`year'_`year_lead' ///
											 if !mi(avg_oud_pop_`year'_`year_lead')
			capture replace oud_pop_`year' = (avg_oud_pop_`year_lag'_`year' + avg_oud_pop_`year'_`year_lead') / 2 ///
											 if !mi(avg_oud_pop_`year_lag'_`year') & ///
												!mi(avg_oud_pop_`year'_`year_lead') 		
			}
		
		* 6.2 - For 2014, Create Constant Growth from 2013 to 2014 and from 2014 to 2015
		replace oud_pop_2014 = oud_pop_2013 * (oud_pop_2015 / oud_pop_2013)^(1/2)
	
	* 7 - Clean Data
	rename stname state
	order state oud_pop_*
	replace state = "DISTRICT OF COLUMBIA" if state == "DISTRICT OFCOLUMBIA"
	
	* 8 - Export Wide Format Data
	compress
	export excel "Output\state_oud_pop_clean.xlsx", sheet("Wide", replace) first(var)
	
	* 9 - Export Long Format Data
	keep state oud_pop_*
	rename oud_pop_* oud_pop*
	reshape long oud_pop, i(state) j(year)
	export excel "Output\state_oud_pop_clean.xlsx", sheet("Long", replace) first(var)
	save "Output\state_oud_pop_clean", replace