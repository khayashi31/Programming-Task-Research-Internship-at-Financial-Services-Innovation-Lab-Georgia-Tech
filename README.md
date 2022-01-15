
# SEC-EDGAR Randomized 8-K Sentiment Analysis 

This program is split into two parts: 

1. Downloads 10 random 8-Ks for each year-quarter from the SEC website for the time period 1995:Q1 through 2021:Q4. 
2. Performs a rudimentary sentiment analysis and generates sentiment score and time-series plot.



## Prerequisites

1. This program was created to run on Mac OS and python 3.10.1.

2. Download data and python dependencies, confirming that they are in the same folder as the program. (KEEP DEFAULT NAMES FOR DEPENDENCIES)
- Link to data file with LM Dictionary: https://drive.google.com/file/d/1moS1tkh_AJafpcIFpktaSvZwrzv5d4ix/view
- Link to module to load Loughran-Mcdonald master dictonary: https://drive.google.com/file/d/1yfRFGfRkJ5rSwDwH-QNB3DjaKxCUeJeR/view

## Installation

To install and run program, follow these steps.

1. Create a new folder on machine and download python file.

2. Download dependencies (see "Prerequisites") and place the files in the same folder as the python program.

3. Open program using an IDE or run through terminal.


    
## Usage

### Changing time span
The selected time span is 1995:Q1 to 2021:Q4. However, you can change this by editing the variables start_year and end_year below the "download" function as shown below.

![Screen Shot 2021-12-21 at 7 37 08 PM](https://user-images.githubusercontent.com/96277691/146917347-6a89f8ce-e44f-4635-8bb3-ac981a511607.png)

### Confirming continuation to next step
After each step of the process, the program will ask if you want to continue to the next step as shown below. When prompted with the questions, type in "yes" or "no".

![Screen Shot 2021-12-21 at 7 49 15 PM](https://user-images.githubusercontent.com/96277691/146918095-d42253bf-c0a3-42ae-9298-2283451fb8ef.png)
![Screen Shot 2021-12-21 at 7 49 35 PM](https://user-images.githubusercontent.com/96277691/146918105-35fde9fe-a5e0-440a-86f4-d607a26d1b24.png)
![Screen Shot 2021-12-21 at 8 01 34 PM](https://user-images.githubusercontent.com/96277691/146919502-2cc8243f-cdeb-4f3c-ba3a-e2c25d58f374.png)



## Examples
The program will perform the following tasks in order.
1. After the desired time span is confirmed, the program will begin downloading all the master.zip files from the SEC website. All zip files will be downloaded to a new folder named "data_files," placed in the same folder as the program. The url to the downloaded files will be printed as shown below.

    ![Screen Shot 2021-12-22 at 8 56 03 AM](https://user-images.githubusercontent.com/96277691/147012510-dde58d5b-2d25-44ca-8442-61ab95f0255f.png)

2. If answered "yes" when prompted "Completed downloading all master.zip files. Unzip the files?" the program will begin to unzip all of the previously downloaded zip files. All unzipped .idx files will be placed in a new folder named "idx_files" in "data_files" folder. The unzipped files' names will be printed as shown below. 

    ![Screen Shot 2021-12-22 at 8 58 16 AM](https://user-images.githubusercontent.com/96277691/147012707-902be3b5-ff3d-4476-9a4d-785babfcf726.png)

3. If answered "yes" when prompted "Continue onto extracting 10 random 8-Ks for each year-quarter?" the program will begin to select and download 10 random 8-K filings for each year quarter. The 8-K files will be placed in a new folder named "8-Ks," contained in the same folder as the program. The url to the selected files will be printed as shown below.

    ![Screen Shot 2021-12-22 at 9 00 50 AM](https://user-images.githubusercontent.com/96277691/147012957-edc9da13-3d64-4b93-8933-9fd32af003e1.png)

4. A csv file, as shown below, containing the information of selected 8-Ks will be created. This can be found in a new folder named "csv_file" which is in the same folder as the program. 

    ![Screen Shot 2021-12-22 at 9 19 04 AM](https://user-images.githubusercontent.com/96277691/147014121-94a75c6c-165a-4c77-a073-9a6e3164bd91.png)

5. If answered "yes" when prompted "Perform rudimentary sentiment analysis on sample data?" the program will being to clean all of the downloaded 8-Ks to reduce noise. The cleaned text is saved as a pickle and can be found in the folder named "cleaned_txt." Then it will compute sentiment scores for each 8-K filings using a bag-of-words approach. 

6. The program will produce a sentiment score and time-series plot as shown below. (From two different randomized samples)

    ![time_and_sentiment_score](https://user-images.githubusercontent.com/96277691/147013266-55cc12d3-d917-46cd-b60f-c5e3b36591ab.jpg)
    ![time_and_sentiment_score](https://user-images.githubusercontent.com/96277691/147018282-3d98d331-ecb1-49b0-a349-37d65f4f7f38.jpg)


7. More descriptive statistics for the sentiment measure calculated can be found in the file "Parser.csv" which can be located in the same folder as the program. "Parser.csv" contains basic %positve/negative words along with additional statistics such as %constraining, %strong/weak modal, %litigious, etc. 



## Thought Process and Challenges

### Selecting and Downloading 10 random 8-K filings
- The third step in this program involved reading through the .idx files, filtering them to keep only the 8-K filings, and extracting/downloading 10 random companies' 8-K filings for each year-quarter. This job is done by the function "eightKdownloader." Filtering through the .idx files takes a relatively long amount of time even when using regex. Still, regex seems to be the fasted and most efficient way to conduct the action.

### Nested Functions
- This program uses nested/inner functions in the "produceStats" function. This was done since the functions "main" and "get_data" required direct access to variables such as "MASTER_DICTIONARY_FILE" and "OUTPUT_FILE" defined in the enclosing function. Additionally, this allows "produceStats" to be run independently on any set of cleaned data files without having to run the whole program. 

### Pickle File
- This program saves the cleaned text files as .pkl files. This was done to increase efficiency: Since the cleaned text files are not meant to be analyzed manually by humans, its main purpose is to be reloaded back into the program. Therefore, serialization was a better option then rewriting the cleaned text onto a .txt file and reading it back into the program later. 



## Credits

"produceStats", the function used to parse through the cleaned data and produce a time-series plot modifies a parser program taken from the University of Notre Dame's Software Repository for Accounting and Finance. The original program can be found through this link: https://sraf.nd.edu/textual-analysis/code/




## Contact

For any questions or concerns, please contact me at: khayashi31@gatech.edu
