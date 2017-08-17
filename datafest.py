from sklearn.externals import joblib
from sklearn.model_selection import ShuffleSplit
from datetime import datetime
import re

def check_dates(holiday_start, holiday_end, start_date, end_date):
	'''
	if holiday_start <= start_date <= holiday_end or holiday_start <= end_date <= holiday_end or (
					holiday_start <= start_date and holiday_end <= end_date) or (
					holiday_start >= start_date and holiday_end >= end_date):
		return True
	return False
	'''
	if (holiday_end - start_date).days < 0 or (holiday_start - end_date).days > 0:
		return False
	return True


def add_holidays():
	springBreak = ["3/1/2015", "3/20/2015"]
	summer = ["7/1/2015", "9/1/2015"]
	holidays = [["12/12/2015", "12/20/2015"], ["7/1/2015", "7/7/2015"], ["12/20/2015", "1/5/2016"],
				["11/1/2015", "11/30/2015"], springBreak, ["2/18/2015", "2/25/2015"],
				["5/1/2015", "5/9/2015"], summer, ["4/2/2015", "4/6/2015"]]

	with open('training_set.txt', 'r') as input_file:
		with open("modified_training_set.txt", "w+") as output_file:

			header = input_file.readline().strip("\n")
			header += "\t" + "is_holiday\n"
			output_file.write(header)
			header = header.split("\t")
			header = [str(i) for i in header]
			user_location_country = header.index("user_location_country")
			srch_ci = header.index("srch_ci")
			srch_co = header.index("srch_co")
			srch_children_cnt = header.index("srch_children_cnt")

			for line in input_file:
				lineSplit = line.strip("\n").split("\t")
				start_date = str(lineSplit[srch_ci])
				end_date = str(lineSplit[srch_co])
				try:

					start_date = datetime.strptime(start_date, "%Y-%m-%d")
					end_date = datetime.strptime(end_date, "%Y-%m-%d")

				except:
					continue

				append = False
				for holiday in holidays:
					holiday_start = datetime.strptime(holiday[0], "%m/%d/%Y")
					holiday_end = datetime.strptime(holiday[1], "%m/%d/%Y")

					if check_dates(holiday_start, holiday_end, start_date, end_date):
						if holiday == summer:
							if int(lineSplit[srch_children_cnt]) > 0:
								append = True

						elif holiday == springBreak:
							if (str(lineSplit[user_location_country]) == "UNITED STATES OF AMERICA" or str(lineSplit[user_location_country]) == "CANADA"):
								append = True

						else:
							append = True

				if append:
					lineSplit.append("1\n")
				else:
					lineSplit.append("0\n")

				output_line = "\t".join(lineSplit)
				output_file.write(output_line)


def remove_latlon():
	with open("modified_data.txt", "r") as file:
		with open('modified_data1.txt', "w+") as outputFile:
			for line in file:
				lineSplit = line.split("\t")

				write = True
				for string in lineSplit:
					if string == "NULL":
						write = False
						continue

				if write:
					outputFile.write("\t".join(lineSplit))


def check_row():
	i = 0.0;
	ii = 0.0;
	with open('data.txt', 'r') as fp:
		next(fp)
		for line in fp:
			ii += 1.0
			test = line.split("\t")
			if test[10] == "1":
				i += 1.0

	print(i/ii)

# def pickle_data(clf, name):
# 	joblib.dump(clf, name)

# def create_dictionary():
# 	clf = {}
# 	with open('dest.txt', 'r') as data:
# 		next(data)
# 		for line in data:
# 			test = line.split("\t")
# 			clf[test[0]] = test[1]
# 	pickle_data(clf, "dest_dictionary.pkl")

def change_feautre():
	clf = joblib.load('dest_dictionary.pkl')
	i = 0.0
	# j = 0.0

	with open('data.txt', 'r') as fp1:
		with open('modified_data.txt', 'w') as fp2:
			for line in fp1:

				line = line.strip("\n")
				test = line.split("\t")

				if i != 0:

					# chec if destination id is found in dest.txt file. clf is the pickled dest.txt file
					if test[17] in clf:

						test[17] = clf[test[17]]

					else:
						# j+=1
						test[17] = "NULL"

					# check time in and time out
					time_in = test[12]
					time_out = test[13]

					try:
						# calculate time difference and create a total time of stay
						date_format = "%Y-%m-%d"
						a = datetime.strptime(time_in, date_format)
						b = datetime.strptime(time_out, date_format)
						total_time = b - a

						# print(total_time.days)
						# print(type(total_time.days))
						# return

						test.append(str(total_time.days))
						

					except ValueError:
						continue

				else:
					test.append("date_diff")
				

				myString = "\t".join(test)
				myString = myString + "\n"
				fp2.write(myString)

				i+=1.0

	# print(j/i)

def create_training_set():
	i = 0
	with open('modified_data.txt', 'r') as input:
		with open('training_set.txt', 'w') as output:
			header = input.readline()
			output.write(header)

			for line in input:

				if i % 1000 == 1:
					output.write(line)
				i+=1

	print("success")

add_holidays()
# change_feautre()
# create_training_set()

