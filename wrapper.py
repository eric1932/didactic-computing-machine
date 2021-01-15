class Wrapper:
    _dict = {}

    @staticmethod
    def get_instance(module_name):
        if module_name not in Wrapper._dict:
            print("Wrapper", "created")  # TODO
            exec("from jobs.%s import Job" % module_name, globals())
            exec("Wrapper._dict[module_name] = Job()", globals(), locals())
        # print("Wrapper", Wrapper._dict[module_name])  # TODO
        return Wrapper._dict[module_name]
