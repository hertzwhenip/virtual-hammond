from math import sin, pi
import wave
from struct import pack

class Synthesizer(object):
	def __init__(self, interpreter_list, organ_registry):
		self.interpreter_list = interpreter_list
		self.durations = self.get_durations(interpreter_list)
		self.frequencies = self.get_frequencies(interpreter_list)
		self.organ_registry_list = self.get_organ_registry(organ_registry)

	def get_durations(self, interpreter_list):
		durations = []
		for i in range(0, len(interpreter_list)):
			durations.append(interpreter_list[i][0])	
		return durations

	def get_frequencies(self, interpreter_list):
		frequencies = []
		for i in range(0, len(interpreter_list)):
			frequencies.append(interpreter_list[i][1])	
		return frequencies

	def get_organ_registry(self, organ_registry):
		organ_registry_list = []
		for value in organ_registry:
			organ_registry_list.append(int(value))
		return organ_registry_list

	def synthesize(self):
		'''
		Method responsible for producing a sequence of samples
		that will represent the wave form of each note.
		'''

		output_samples = []
		output = []

		for i in range(0, len(self.interpreter_list)):
			output_samples.append(self.get_samples(self.organ_registry_list, self.durations[i], self.frequencies[i]))

		normalized_output_samples = self.normalize(output_samples)

		for i in range(0, len(self.interpreter_list)):
			output.append({'freq': self.frequencies[i], 'samples': normalized_output_samples[i]})

		return output

	def get_samples(self, org_reg_list, duration, frequency):
		'''
		Method responsible for producing the samples of a note
		taking into consideration the amplitude, duration
		and the frequency.

		Returns a list of the samples of a note.
		'''
		rate = 44100
		data = []
		mult_frequencies = self.get_mult_freq(frequency)

		for i in range(0, int(rate*duration)):
			data.append(self.get_one_sample(org_reg_list, mult_frequencies, rate, i))
		return data

	def get_one_sample(self, org_reg_list, mult_frequencies, rate, i):
		value = 0
		for j in range(0, len(org_reg_list)):
			value += org_reg_list[j]/8 * sin(2*pi*mult_frequencies[j]*i/rate)
		return value

	def get_mult_freq(self, freq):
		values = [1/2.0, 2/3.0 , 1, 2, 3, 4, 5, 6, 8]
		data = []
		for value in values:
			data.append(value*freq)
		data = map(int, data)
		return data

	def normalize(self, data):
		'''
		Method responsible for normalizing the samples.
		'''
		MAX_VALUE = 2 ** 15 - 1  #32767
		maximum = 0

		for k in data:
			for v in k:
				if abs(v) > maximum:
					maximum = abs(v)

		if not maximum == 0:
			normalize_factor = (float(MAX_VALUE)/ maximum)

		normalized_data = []
		tmp = []
		for i in data:
			tmp = []
			for values in i:
				tmp.append(values * normalize_factor)
			normalized_data.append(tmp)
		return normalized_data

####__APAGAR


if __name__ == "__main__":
	expected_result = [
	(0.5625, 1046),
	(0.3750, 1318),
	(0.3750, 1479),
	(0.1875, 1760),
	(0.5625, 1567),
	(0.3750, 1318),
	(0.3750, 1046),
	(0.1875, 880),
	(0.1875, 739),
	(0.1875, 739),
	(0.1875, 739),
	(0.7500, 783),
	(0.1875, 0),
	(0.1875, 0),
	(0.1875, 523),
	(0.1875, 523),
	(0.1875, 739),
	(0.1875, 739),
	(0.1875, 739),
	(0.1875, 783),
	(0.5625, 932),
	(0.1875, 1046),
	(0.1875, 1046),
	(0.1875, 1046),
	(0.3750, 1046)
]
	a = Synthesizer(expected_result, "888888888")
	data = a.synthesize()

	wav = wave.open("test123.wav", 'w')
	wav.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))

	samples = []
	output1 = []
	for i in data:
		output1.extend(i['samples'])
		print len(i['samples'])
	print len(output1)