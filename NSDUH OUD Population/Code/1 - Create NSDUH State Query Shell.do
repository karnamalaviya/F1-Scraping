/*****************************************
* Purpose:    Create Shell of Queries to Pull from NSDUH
* Date:       4 May 2020
*****************************************/

cd "[configure]" 

*************************************** 
*   Shell of States with NSDUH Data   *	
***************************************

	* 1 - Input State Names
	clear
	input str50 state
	"ALABAMA"
	"ALASKA"
	"ARIZONA"
	"ARKANSAS"
	"CALIFORNIA"
	"COLORADO"
	"CONNECTICUT"
	"DELAWARE"
	"DISTRICT OF COLUMBIA"
	"FLORIDA"
	"GEORGIA"
	"HAWAII"
	"IDAHO"
	"ILLINOIS"
	"INDIANA"
	"IOWA"
	"KANSAS"
	"KENTUCKY"
	"LOUISIANA"
	"MAINE"
	"MARYLAND"
	"MASSACHUSETTS"
	"MICHIGAN"
	"MINNESOTA"
	"MISSISSIPPI"
	"MISSOURI"
	"MONTANA"
	"NEBRASKA"
	"NEVADA"
	"NEW HAMPSHIRE"
	"NEW JERSEY"
	"NEW MEXICO"
	"NEW YORK"
	"NORTH CAROLINA"
	"NORTH DAKOTA"
	"OHIO"
	"OKLAHOMA"
	"OREGON"
	"PENNSYLVANIA"
	"RHODE ISLAND"
	"SOUTH CAROLINA"
	"SOUTH DAKOTA"
	"TENNESSEE"
	"TEXAS"
	"UTAH"
	"VERMONT"
	"VIRGINIA"
	"WASHINGTON"
	"WEST VIRGINIA"
	"WISCONSIN"
	"WYOMING"
	end
	compress
	
	* 2 - Clean State Names For Use in URLs
	replace state = trim(upper(subinstr(state, " ", "+", .)))
	
	* 3 - Prepare for Merge with NSDUH Queries Dataset
	count 
	local expand_num `r(N)'
	gen n = _n

	* 4 - Save
	compress
	tempfile states
	save `states'

	
****************************************** 
*   Create State-Level Queries Dataset   *	
******************************************
	
	
	import delimited "Input\NSDUH Queries.csv", clear varnames(1)
	
	* 1 - Set Unique Identifier for Each Query
	gen query_num = _n
	
	* 2 - Expand Query To Create One Per State
	expand `expand_num'
	
	* 3 - Merge in State Names
	bysort query_num : gen n = _n
	merge m:1 n using `states', nogen
	
	* 4 - Clean 
	drop n
	order surveyyear* state
	sort query_num state
	
	* 5 - Export as .csv
	compress
	export delimited "Input\State NSDUH Queries.csv", replace
