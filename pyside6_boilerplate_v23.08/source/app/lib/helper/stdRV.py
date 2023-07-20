#Standard library modules
import base64
import json

#Third-party modules
import numpy as np
import pandas as pd

#Custom modules
class StdRV():
	def encode(var):
		return json.dumps(StdRV.encodeElement(var))		

	def encodeElement(var):
		varType = type(var).__name__
		if varType == "dict":
			rv = StdRV.encodeDict(var)
		elif varType == "list":
			rv = StdRV.encodeList(var)
		elif varType in ["int","int64"]:
			rv = StdRV.encodeInt(var)
		elif varType in ["float","float64"]:
			rv = StdRV.encodeFloat(var)
		elif varType == "str":
			rv = StdRV.encodeStr(var)
		elif varType == "DataFrame":
			rv = StdRV.encodeDataFrame(var)
		elif varType == "ndarray":
			rv = StdRV.encodeNdarray(var)
		else:
			rv = None
		return rv

	def encodeDict(dict_var):
		rv = {"dtype":"dict","value":{}}
		for varName in dict_var.keys():
			rv["value"][varName] = StdRV.encodeElement(dict_var[varName])
		return rv

	def encodeList(list_var):
		rv = {"dtype":"list","value":[]}
		for var in list_var:
			rv["value"].append(StdRV.encodeElement(var))
		return rv

	def encodeInt(n_var):
		rv = {"dtype":"int","value":str(n_var)}
		return rv

	def encodeFloat(d_var):
		rv = {"dtype":"float","value":str(float(d_var))}
		return rv

	def encodeStr(s_var):
		rv = {"dtype":"str","value":s_var}
		return rv

	def encodeDataFrame(df_var):
		df_json = df_var.to_json()
		rv = {"dtype":"DataFrame","value":df_json}
		return rv

	def encodeNdarray(arr_var):
		array = np.ascontiguousarray(arr_var).astype(float)
		b64str_var = base64.b64encode(array).decode('ascii')
		rv = {"dtype":"ndarray","value":b64str_var,"shape":array.shape}
		return rv

	def decode(json_var):
		var = json.loads(json_var)
		return StdRV.decodeElement(var)

	def decodeElement(var):
		varType = var["dtype"]
		if varType == "dict":
			rv = StdRV.decodeDict(var)
		elif varType == "list":
			rv = StdRV.decodeList(var)
		elif varType == "int":
			rv = StdRV.decodeInt(var)
		elif varType == "float":
			rv = StdRV.decodeFloat(var)
		elif varType == "str":
			rv = StdRV.decodeStr(var)
		elif varType == "DataFrame":
			rv = StdRV.decodeDataFrame(var)
		elif varType == "ndarray":
			rv = StdRV.decodeNdarray(var)
		else:
			rv = None
		return rv

	def decodeDict(var):
		dict_var = var["value"]
		rv = {}
		for varName in dict_var.keys():
			rv[varName] = StdRV.decodeElement(dict_var[varName])
		return rv

	def decodeList(var):
		list_var = var["value"]
		rv = []
		for var_el in list_var:
			rv.append(StdRV.decodeElement(var_el))
		return rv

	def decodeInt(var):		
		return int(var["value"])

	def decodeFloat(var):
		rv = float(var["value"])
		return rv

	def decodeStr(var):
		return str(var["value"])

	def decodeDataFrame(var):
		return pd.read_json(var["value"])

	def decodeNdarray(var):
		b64_str_value = var["value"]
		shape = var["shape"]
		s = np.frombuffer(base64.decodebytes(b64_str_value.encode('ascii')))
		arr = s.reshape(*shape)
		return arr
