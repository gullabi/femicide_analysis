#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv, codecs, sys

def readLines(outfile, delimiter):
    data = []
    for line in outfile:
        data.append(line.strip().split(delimiter))
    return data

def getCsv(data):
	out_data = []
	data_dict = {}
	for i in range(len(data)):
		if i == 0: # assuming there is a header
			keys = data[i] # Title\tWolf Title\tArtist\tGenre\tISRC\twolf_id\twolf_artist_id
		else:
			for j in range(len(keys)):
				try:
					data_dict[keys[j]] = data[i][j]
				except:
					print('WARNING line %s not normalized, substituting empty string. '%data[i])
					data_dict[keys[j]]= ''
					pass
			out_data.append(data_dict)
			data_dict = {}
	return keys, out_data

def getCsvReader(filename, delimiter, line_start=0):
	out_data = []
	data_dict = {}

	fin = codecs.open(filename, 'rU')#, encoding='utf8')
	reader = csv.reader(fin, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)
	i = 0
	for row in reader:
		if i < line_start+1:
			keys = row
		else:
			for j in range(len(keys)):
				try:
					data_dict[keys[j]] = row[j].strip()
				except:
					print('WARNING line %s not normalized, substituting empty string. '%row)
					data_dict[keys[j]]= ''
					pass
			out_data.append(data_dict)
			data_dict = {}
		i += 1
	return keys, out_data


def csvFormattedOut(row,keys):
	'''
	row in dictionary
	keys in list

	converts rows to a list with the key order
	'''
	lst = []
	for key in keys:
		#try:
		lst.append(row[key])
		#except:
			#not found substuting empty string
			#lst.append('""')
	return lst


def outCsv(keys, data, csv_out_name, delimiter=','):
	csv_out = codecs.open(csv_out_name, 'w+')
	out_writer = csv.writer(csv_out, delimiter=delimiter, quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
	out_writer.writerow(keys)
	for d in data:
		for key in keys:
			try:
				d[key]
			except:
				d[key] = ''
				#print key, d[key]
		try:
			out_writer.writerow(csvFormattedOut(d,keys))
		except:
			print("line could not be written with error: %s"%sys.exc_info()[0])
			print("> with keys: %s"%'\t'.join(d.keys()))
			for k in d.keys():
				print("%s: %s"%(k, d[k]),)
			print
			#print "> %s"%'\t'.join(d)
			sys.exit()
	csv_out.close()

def outCsvInfo(keys, data, csv_out_name):
	csv_out = codecs.open(csv_out_name, 'w+')
	out_writer = csv.writer(csv_out, delimiter=',', quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
	out_writer.writerow(keys)
	for info in data:
		d = info[1]
		for key in keys:
			try:
				d[key]
			except:
				d[key] = ''
				#print key, d[key]
		try:
			out_writer.writerow(csvFormattedOut(d,keys))
		except:
			print("line could not be written with error: %s"%sys.exc_info()[0])
			print("> with keys: %s"%'\t'.join(d.keys()))
			for k in d.keys():
				print("%s: %s"%(k, d[k]), )
			print
			#print "> %s"%'\t'.join(d)
			#sys.exit()
	csv_out.close()
