import numpy
import pandas
import datetime

def condense(infile='data_1000.txt', outfile='data_condensed.txt', session_length=datetime.timedelta(1)):
	print("reading table...")
	df = pandas.read_table(infile)
	print("done reading table.")
	df['date_time'] = pandas.to_datetime(df['date_time'])
	print("sorting data...")
	df_sorted = df.sort(['user_id','date_time'])
	print("sorted data")
	curr_user = df.head(1)['user_id'][0]
	curr_date = df.head(1)['date_time'][0]
	curr_row = df.head(1)
	curr_clicks = df.head(1)['cnt'][0]
	out = open(outfile,'w')
	print("writing new file...")
	out.write('user_id\tdate\tbooked\tclicks\t')
	out.write(write_header())
	for index, row in df_sorted.iterrows():
		if row['user_id'] != curr_user:
			date_formatted = curr_date.strftime("%m/%d/%Y")
			out.write( "{0}\t{1}\t{2}\t{3}\t".format(curr_user, date_formatted, curr_row['is_booking'], curr_clicks) )
			out.write(line_to_write(curr_row))
			curr_date = row['date_time']
			curr_user = row['user_id']
			curr_clicks = 0
		else:
			if row['date_time']-curr_date > session_length:
				date_formatted = curr_date.strftime("%m/%d/%Y")
				out.write( "{0}\t{1}\t{2}\t{3}\t".format(curr_user, date_formatted, curr_row['is_booking'], curr_clicks) )
				out.write(line_to_write(curr_row))
				curr_date = row['date_time']
				curr_clicks = 0
		curr_row = row
		curr_clicks += row['cnt']
	out.close()
	print("wrote new file")
	return


def line_to_write(row):
	s = ""
	for var in var_list:
		try:
			s += str(row[var]) + "\t"
		except:
			s += str(1) + "\t"
	s += "\n"
	return s

def write_header():
	s = ""
	for var in var_list:
		s += var + "\t"
	s += "\n"
	return s


var_list = [
'user_location_country',
'orig_destination_distance',
'is_mobile',
'is_package',
'channel',
'srch_adults_cnt',
'srch_children_cnt',
'srch_rm_cnt',
'srch_destination_id',
'hotel_id',
'prop_is_branded',
'prop_starrating',
'distance_band',
'hist_price_band',
'popularity_band',
'cnt',
'date_diff',
'is_holiday']

condense()












