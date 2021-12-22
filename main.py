import csv
import glob
import matplotlib.pyplot as plt
import os
import pickle
import random
import re
import requests
import string
import sys
import zipfile
import datetime as dt
from nltk import word_tokenize

# user-agent must be declared when requesting to SEC-EDGAR
heads = {'Host': 'www.sec.gov', 'Connection': 'close',
         'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
         }

wd = os.getcwd()
working_directory: str = wd[:]
print("Working directory: " + working_directory)





def produceStats():
    """
    Program to provide generic parsing for all cleaned data files.
    
    Dependencies:
        Python: MOD_Load_MasterDictionary_v2020.py
        Data: LoughranMcDonald_MasterDictionary_2020.csv
        
    Outputs:
        a. Graph plotting average sentiment score over time
        b. csv file containing:
            1.  File name
            2.  File size (in bytes)
            3.  Number of words (based on LM_MasterDictionary
            4.  Proportion of positive words (use with care - see LM, JAR 2016)
            5.  Proportion of negative words
            6.  Proportion of uncertainty words
            7.  Proportion of litigious words
            8.  Proportion of modal-weak words
            9.  Proportion of modal-moderate words
            10.  Proportion of modal-strong words
            11.  Proportion of constraining words (see Bodnaruk, Loughran and McDonald, JFQA 2015)
            12.  Number of alphanumeric characters (a-z, A-Z)
            13.  Number of digits (0-9)
            14.  Number of numbers (collections of digits)
            15.  Average number of syllables
            16.  Average word length
            17.  Vocabulary (see Loughran-McDonald, JF, 2015)
        
    """

    sys.path.append(working_directory)
    import MOD_Load_MasterDictionary_v2020 as LM

    MASTER_DICTIONARY_FILE = working_directory + r"/LoughranMcDonald_MasterDictionary_2020.csv"
    OUTPUT_FILE = working_directory + r"/Parser.csv"
    OUTPUT_FIELDS = ['file name', 'file size', 'number of words', '% negative', '% positive',
                 '% uncertainty', '% litigious', '% strong modal', '% weak modal',
                 '% constraining', '# of alphabetic', '# of digits',
                 '# of numbers', 'avg # of syllables per word', 'average word length', 'vocabulary']
    lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, print_flag=True)

    # Creating a list of files to analyze
    TARGET_FILES_LIST = []
    os.chdir('cleaned_txt')
    rootdir = working_directory + r"/cleaned_txt"
    count = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file == ".DS_Store":
                continue
            TARGET_FILES_LIST.append(subdir + "/" + file)
            TARGET_FILES = TARGET_FILES_LIST[count]
            count += 1


            def main():
                """ Main function to go through cleaned files and extract data. """

                if not os.path.isfile(OUTPUT_FILE):
                    f_out = open(OUTPUT_FILE, 'w')
                    wr = csv.writer(f_out, lineterminator='\n')
                    wr.writerow(OUTPUT_FIELDS)
                else:
                    f_out = open(OUTPUT_FILE, 'a')
                    wr = csv.writer(f_out, lineterminator='\n')

                file_list = glob.glob(TARGET_FILES)
                n_files = 0
                for file in file_list:
                    n_files += 1
                    print(f'{n_files:,} : {file}')
                    with open(file, 'r', encoding='UTF-8', errors='ignore') as f_in:
                        doc = f_in.read()
                    doc = re.sub('(May|MAY)', ' ', doc)  # drop all May month references
                    doc = doc.upper()  # for this parse caps aren't informative so shift

                    output_data = get_data(doc)
                    output_data[0] = file
                    output_data[1] = len(doc)
                    wr.writerow(output_data)
                    if n_files == 3: break


            def get_data(doc):
                """ Function to connect to LM dictionary and get scores for each word. """

                vdictionary = dict()
                _odata = [0] * 16
                total_syllables = 0
                word_length = 0

                tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words
                for token in tokens:
                    if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
                        _odata[2] += 1  # word count
                        word_length += len(token)
                        if token not in vdictionary:
                            vdictionary[token] = 1
                        if lm_dictionary[token].negative: _odata[3] += 1
                        if lm_dictionary[token].positive: _odata[4] += 1
                        if lm_dictionary[token].uncertainty: _odata[5] += 1
                        if lm_dictionary[token].litigious: _odata[6] += 1
                        if lm_dictionary[token].strong_modal: _odata[7] += 1
                        if lm_dictionary[token].weak_modal: _odata[8] += 1
                        if lm_dictionary[token].constraining: _odata[9] += 1
                        total_syllables += lm_dictionary[token].syllables

                _odata[10] = len(re.findall('[A-Z]', doc))
                _odata[11] = len(re.findall('[0-9]', doc))
                # drop punctuation within numbers for number count
                doc = re.sub('(?!=[0-9])(\.|,)(?=[0-9])', '', doc)
                doc = doc.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
                _odata[12] = len(re.findall(r'\b[-+\(]?[$€£]?[-+(]?\d+\)?\b', doc))
                _odata[13] = total_syllables / _odata[2]
                _odata[14] = word_length / _odata[2]
                _odata[15] = len(vdictionary)

                # Convert counts to %
                for i in range(3, 10 + 1):
                    _odata[i] = (_odata[i] / _odata[2]) * 100
                # Vocabulary

                return _odata


            if __name__ == '__main__':
                start = dt.datetime.now()
                print(f'\n\n{start.strftime("%c")}\nPROGRAM NAME: {sys.argv[0]}\n')
                main()
                print(f'\n\nRuntime: {(dt.datetime.now() - start)}')
                print(f'\nNormal termination.\n{dt.datetime.now().strftime("%c")}\n')


    def analyze():
        """ Function to go through 'Parser.csv' to return a dictionary containing year - average sentiment score pairs. """

        os.chdir(working_directory)
        try:
            file = open('Parser.csv')
        except FileNotFoundError:
            return "Parser.csv does not exist in the same folder as the program."

        csvreader = csv.reader(file)
        header = next(csvreader)
        time_sentiment_dict = {}
        for row in csvreader:
            sentiment_score = float(row[4]) - float(row[3])
            time = re.findall(r'cleaned_txt/(.*?)QTR', row[0])[0]
            if time not in time_sentiment_dict:
                time_sentiment_dict[time] = [sentiment_score]
            else:
                time_sentiment_dict[time].append(sentiment_score)

        # get average year_avg_dict contains year and average pair
        year_avg_dict = {}
        for year in time_sentiment_dict:
            count = 0
            total_sentiment_score = 0
            for score in time_sentiment_dict[year]:
                total_sentiment_score += score
                count += 1
            average = total_sentiment_score / count
            year_avg_dict[int(year)] = average

        return year_avg_dict


    def graph(year_avg_dict):
        """ Function to produce scatter plot. """

        years = list(year_avg_dict.keys())
        avgs = list(year_avg_dict.values())

        plt.scatter(years, avgs)
        plt.xlabel("Years")
        plt.ylabel("Average Sentiment Score (%)")
        plt.title("Average Sentiment Score over time")
        os.chdir(working_directory)
        plt.savefig("time_and_sentiment_score.jpg")
        plt.show()

    graph(analyze())




def cleanData(path):
    """
    Cleans and removes HTML for selected 8-K files.
    Cleaned files are saved as pickles in 'cleaned_txt' folder in working_directory.
    """

    file = open(path, 'rt')
    text = file.read()
    file.close()

    # clean file
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]  # remove remaining tokens that are not alphabetic

    # create new folder 'cleaned_txt' and save data as .pkl
    final_directory = os.path.join(working_directory, r'cleaned_txt/' + re.findall(r'/8-Ks/(.*?)/', path)[0])
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    new_file_name = re.findall(r'8-Ks/(.*?).txt', path)[0].split("/")[1]
    with open(f'{final_directory}/{new_file_name}.pkl', 'wb') as f:
        pickle.dump(words, f)

    print("Cleaned: " + new_file_name)






def eightKdownloader():
    """
    Reads through .idx file, extracts 8-K filings, selects 10 random companies and downloads corresponding 8-Ks.
    Creates new folder '8-Ks' in working_directory organized by year-quarter.
    Creates new folder 'csv_file' in working_directory containing .csv file with selected companies' data
    """

    eK_working_directory = working_directory + "/data_files/idx_files"

    final_csv_directory = os.path.join(working_directory, r'csv_file')
    if not os.path.exists(final_csv_directory):
        os.makedirs(final_csv_directory)  # create new folder 'csv_file' in working_directory


    # year-quarter along with company name, cik, and filing date for selected 8-Ks will be added to csv file
    header = ["year", "quarter", "company_name", "cik", "filing_date"]
    with open(f'{final_csv_directory}/csv_file.csv', 'w') as c:
        writer = csv.writer(c)
        writer.writerow(header)


    # extracting and selecting 8-Ks for each .idx file
    for file in sorted(os.listdir(eK_working_directory)):
        os.chdir(eK_working_directory)
        with open(file, "rb") as f:
            idx_data = f.read().decode("utf-8", "ignore")
            f.close()
            print("Downloading 10 random 8-K files from: " + file)


            # creating list of company names, ciks, filing dates, and 8-K download urls
            company_list = re.findall(r'\|(.*?)\|8-K', idx_data)

            cik_list = re.findall(r'\n(.*?)\|8-K', idx_data)
            for index, pair in enumerate(cik_list):
                cik = pair.split("|")[0]
                cik_list[index] = cik

            date_endpoint_list = re.findall(r'\|8-K(.*?).txt', idx_data)
            date_list = []
            endpoint_list = []
            for line in date_endpoint_list:
                date = line.split("|", 2)[1]
                endpoint = "https://www.sec.gov/Archives/" + line.split("|", 2)[2] + ".txt"
                date_list.append(date)
                endpoint_list.append(endpoint)

            # choosing 10 random companies
            rand_company_list = []
            rand_endpoint_list = []
            rand_cikdate_list = []

            random_index_list = random.sample((range(len(company_list))), 10)
            for index in random_index_list:
                rand_company = company_list[index]
                rand_company_list.append(rand_company)
                rand_endpoint = endpoint_list[index]
                rand_endpoint_list.append(rand_endpoint)
                rand_cik = cik_list[index]
                rand_date = date_list[index]
                rand_cikdate = (rand_cik, rand_date)
                rand_cikdate_list.append(rand_cikdate)


            # downloading the corresponding 8-K files
            for index, link in enumerate(rand_endpoint_list):
                response = requests.get(link, headers=heads)
                print("Downloading: " + link)
                response.raise_for_status()
                yearquart = file.strip("master.idx")
                company = rand_company_list[index]
                if "/" in company:
                    company = company.replace("/", "_")
                os.chdir(working_directory)
                final_txt_directory = os.path.join(working_directory, r'8-Ks/' + yearquart)
                if not os.path.exists(final_txt_directory):
                    os.makedirs(final_txt_directory)
                with open(f'{final_txt_directory}/{company}.txt', 'wb') as f:
                    f.write(response.content)

                # write data onto csv file
                year = yearquart.split("QTR")[0]
                qtr = yearquart.split("QTR")[1]
                csv_data = [year, qtr, company, rand_cikdate_list[index][0], rand_cikdate_list[index][1]]
                with open(f'{final_csv_directory}/csv_file.csv', 'a') as c:
                    writer = csv.writer(c)
                    writer.writerow(csv_data)

    print("Completed downloading all 8-K files. ")
    answer = input("Perform rudimentary sentiment analysis on sample data? \nEnter yes or no: ")
    if answer == "yes":
        print("Starting to clean 8-K files")
        os.chdir('8-Ks')
        rootdir = working_directory + r"/8-Ks"
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                if file == ".DS_Store":
                    continue
                cleanData(subdir + "/" + file)
        os.chdir(working_directory)
        print("Analyzing data...")
        produceStats()

    elif answer == "no":
        print("Ending program.")
        sys.exit()
    else:
        print("Please enter yes or no.")





def extractor():
    """ Extracts idx files from zipped files in 'data_files' folder. """

    extractor_working_directory = working_directory + "/data_files"
    os.chdir(extractor_working_directory)

    final_directory = os.path.join(extractor_working_directory, r'idx_files/')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory) # create new folder 'idx_files' in 'data_files'

    # going through all .zip files in 'data_files' folder
    for file in sorted(os.listdir(extractor_working_directory)):
        if zipfile.is_zipfile(file):
            with zipfile.ZipFile(file) as item:  # treat the file as a zip
                item.extractall()
                print("Unzipped: " + file)
                old_name = extractor_working_directory + "/master.idx"
                new_name = final_directory + file.strip(".zip") + "master.idx"

                # enclosing renaming in try-except
                try:
                    os.rename(old_name, new_name)
                except FileExistsError:
                    print("File already Exists")
                    print("Removing existing file")
                    os.remove(new_name)  # forceful renaming
                    os.rename(old_name, new_name)
                    print('Done renaming a file')

    print("Unzipped all files in 'data_files' folder. ")

    answer = input("Continue onto extracting 10 random 8-Ks for each year-quarter? \nEnter yes or no: ")
    if answer == "yes":
        print("Preparing to download 8-Ks.")
        eightKdownloader()
    elif answer == "no":
        print("Ending program.")
        sys.exit()
    else:
        print("Please enter yes or no.")


def download(year):
    """
    Downloads master.zip files for each year-quarter of specified years.

        Parameters:
            year(int): selected year to download master.zip files for
    """

    for qtr in range(1,5):
        url = f"https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{qtr}/master.zip"
        response = requests.get(url, headers=heads)
        print("Downloading: " + url)
        response.raise_for_status()

        final_directory = os.path.join(working_directory, r'data_files')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)  # create new folder 'data_files' in working_directory

        with open(f'{final_directory}/{year}QTR{qtr}.zip', 'wb') as f:
            f.write(response.content)

start_year = 1995
end_year = 2021

# call download function for specified years
for i in range(start_year, end_year + 1):
    download(i)


answer = input("Completed downloading all master.zip files. Unzip the files? \nEnter yes or no: ")
if answer == "yes":
    print("Extracting idx files from zipped files.")
    extractor()
elif answer == "no":
    print("Ending program.")
    sys.exit()
else:
    print("Please enter yes or no.")








