import json as _json

class test_input_parameter:
    def __init__(self, parameter_name : str, parameter_value):
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value

    def to_dict(self) -> dict:
        return {"parameter_name": self.parameter_name, "parameter_value": self.parameter_value}

    def from_dict(self, d : dict ) -> None:
        self.parameter_name = d["parameter_name"]
        self.parameter_value = d["parameter_value"]

    def __repr__(self) -> str:
        return f"test_input_parameter(name={self.parameter_name}, value={self.parameter_value})"

class test_output_parameter:
    def __init__(self, parameter_name : str, parameter_value):
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value

    def from_dict(self, d : dict) -> None:
        self.parameter_name = d["parameter_name"]
        self.parameter_value = d["parameter_value"]

    def to_dict(self) -> dict:
        return {"parameter_name": self.parameter_name, "parameter_value": self.parameter_value}

    def __repr__(self) -> str:
        return f"test_output_parameter(name={self.parameter_name}, value={self.parameter_value})"

class test_output_file:
    def __init__(self, file_path : str =None, file_type : str =None):
        self.file_path = file_path
        self.file_type = file_type

    def to_dict(self) -> dict:
        return {"file_path": self.file_path, "file_type": self.file_type}

    def from_dict(self, d : dict) -> None:
        self.file_path = d["file_path"]
        self.file_type = d["file_type"]

    def __repr__(self):
        return f"test_output_file(file_path={self.file_path}, file_type={self.file_type})"

class test_entry:
    def __init__(self,
                 test_name      : str = None,
                 test_file_path : str = None,
                 nprimary       : int = 0,
                 runtime        : int =0):
        self.name = test_name
        self.file_path = test_file_path
        self.nprimary = nprimary
        self.runtime = runtime
        self.input_parameters = []
        self.output_parameters = []
        self.output_files = []

    def add_input_parameter(self, parameter_name, parameter_value) -> None:
        self.input_parameters.append(test_input_parameter(parameter_name, parameter_value))

    def add_input_parameter_dict(self, pdict) -> None:
        for k in pdict:
            self.add_input_parameter(k, pdict[k])

    def add_output_parameter(self, parameter_name, parameter_value) -> None:
        self.output_parameters.append(test_output_parameter(parameter_name, parameter_value))

    def add_output_parameter_dict(self, pdict) -> None:
        for k in pdict:
            self.add_output_parameter(k, pdict[k])

    def add_output_file(self, file_path, file_type) -> None:
        self.output_files.append(test_output_file(file_path, file_type))

    def add_output_file_dict(self, fdict) -> None:
        for k in fdict:
            self.add_output_file(k, fdict[k])
            
    def from_dict(self, d) -> None:
        self.name = d["name"]
        self.file_path = d["file_path"]
        self.nprimary = d["nprimary"]
        self.runtime = d["runtime"]
        for v in d["input_parameters"]:
            p = test_input_parameter(None, None)
            p.from_dict(v)
            self.input_parameters.append(p)

        for v in d["output_parameters"]:
            o = test_output_parameter(None, None)
            o.from_dict(v)
            self.output_parameters.append(o)

        for v in d["output_files"]:
            f = test_output_file(None, None)
            f.from_dict(v)
            self.output_files.append(f)

    def to_dict(self):
        d = {
            "name": self.name,
            "file_path": self.file_path,
            "nprimary": self.nprimary,
            "runtime": self.runtime,
            "input_parameters": [p.to_dict() for p in self.input_parameters],
            "output_parameters": [o.to_dict() for o in self.output_parameters],
            "output_files": [o.to_dict() for o in self.output_files]
        }
        return d

    def __repr__(self) -> str:
        s =  f"test_entry(name={self.name}, file_path={self.file_path}, nprimary={self.nprimary}\n"
        s += f"input_parameters={repr(self.input_parameters)}\n"
        s += f"output_parameters={repr(self.output_parameters)}\n"
        s += f"output_files={repr(self.output_files)})"
        return s

class test_entry_store:
    def __init__(self):
        self.entries = []

    def append(self, entry : test_entry) -> None:
        self.entries.append(entry)

    def __len__(self) -> int:
        return len(self.entries)

    def __getitem__(self, index : int) -> test_entry:
        return self.entries[index]

    def __setitem__(self, index : int, value) -> None:
        self.entries[index] = value

    def write_json(self, file_name : str) -> None:
        with open(file_name, "w") as f:
            f.write("[")
            for i, entry in enumerate(self.entries):
                _json.dump(entry.to_dict(), f)
                if i != len(self.entries)-1 :
                    f.write(",\n")
                else :
                    f.write("\n")
            f.write("]")

    def read_json(self, file_name : str) -> None:
        with open(file_name, "r") as f:
            d = _json.load(f)
            self.from_dict(d)

    def from_dict(self, d : dict) -> None:
        # loop over entries

        self.entries = []
        for e in d :
            et = test_entry()
            et.from_dict(e)
            self.append(et)

    def __repr__(self) -> str:
        s = "["
        for e in self.entries :
            s += repr(e) + ","

        s += "]"
        return s

def copy_regression_data(file_name   : str   = "./regression_data.dat",
                         destination : str = "../regression_data/data/") -> None :
    tes = test_entry_store()
    tes.read_json(file_name)

def compare_regression_data(path1       : str  = "./regression_data.dat",
                            path2       : str  = None,
                            output_path : str = None) -> None :
    pass

def html_regression_data(path1 : str = "./regression_data.dat") -> None :
    pass

