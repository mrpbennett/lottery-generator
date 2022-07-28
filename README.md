# Euro Millions Analysis

As a fun little project that will hopefully make me millions one day...I decided to create this little script, that can be called via a FastAPI connection then presented on React frontend.

## What does it do?

### download_latest_lotto_draw_file()

First it takes the lastest draw information from the National Lottery's website via a `.csv` and downloads it, a Pandas dataframe is then created extracting what is needed from the downloaded file.

The extracted data is then put into a supabase table so I can deal with it later.

### drawn_lotto_numbers()

Then the script collects the draw history from the supabase table, and puts all the numbers from the rows into one giant list and returns it as a dictonary so we can use it later.

### collect_duplicate_lotto_numbers()

Taking the returned list from `drawn_lotto_numbers`  I then using `Counter` to count the most common numbers from the dictonary that was returned from `drawn_lotto_numbers`. The common numbers are then returned as a dictonary.

### common_number_lotto_generator()

Lastly takes the top 6 numbers from `get_highest_lotto_count` which takes the 2nd index of each tuple from the returned dictonary from `collect_duplicate_lotto_numbers` and places them into a list and returns the first 6 numbers.

Then we generate a dataset from `collect_duplicate_lotto_numbers()` again, allowing us to compare and generates a list from the all the numbers from the 1st index in the tuple that have the same 2nd index. 

Then a randomly generated 6 digit number is returned consisting of the most commonly drawn numbers from the dataset.