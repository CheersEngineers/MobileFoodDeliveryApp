**Test case 1 Search restaurants by filters**

[UAT][TC-A1] Search returns only 1 matching restaurant instead of expected 2

**Environment**
- App version: 3.1 
- Environment: local 
- OS / Browser / Device: Windows 11, Chrome
- Test data seed: seed_2025_12_14 (expected to include 2 Japanese Downtown restaurants with rating >= 4.0)

**Steps to reproduce**
1. Ensure test data is seeded with at least two Japanese restaurants located in "Downtown" and rating >= 4.0.  
2. Start the app in the test environment.  
3. Open the Search screen.  
4. Enter `cuisine = Japanese`, `location = Downtown`, `rating = 4.0`.  
5. Tap/Search to run the query.  
6. Observe the returned list.

**Test case ID**
TC-A1

**Expected result**
The search returns **both** Japanese restaurants in Downtown (2 items). Results must contain only restaurants matching the filters and complete within the expected time threshold.

**Actual result**
Only **1** matching restaurant is returned. The second restaurant that meets the filter criteria is missing from the results list.

**Severity**
High

**Frequency**
Always (reproduced consistently in current test environment)

**Notes**
- Test performed by John Doe on 2025-12-14 at ~14:00 EET.  
- The missing restaurant record exists in the seeded dataset and appears in the database when inspected directly.  
- Possible areas to check: filter mapping in `RestaurantSearch.search_restaurants`, `browsing.search_by_filters` implementation, rating comparison logic (>= vs >), and any pagination or result-size limits applied after filtering.

**Assigned to**
backend-team / search-feature-owner
