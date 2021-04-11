class latexEnv:
    def __init__(self, command, args=None, opt_args=None, children=None, **kwargs):
        if args is None:
            self.args = {}
        else:
            self.args = args
        if opt_args is None:
            self.opt_args = {}
        else:
            self.opt_args = opt_args
        if children is None:
            self.children = []
        elif not isinstance(children, list):
            self.children = [children]
        else:
            self.children = children
        self.command = command

    def to_latex(self):
        latex_open = "\\begin"
        latex_open += f"{{{self.command}}}"
        latex_open += "".join([f"[{optarg}]" for optarg in self.opt_args.values()])
        latex_open += "".join([f"{{{arg}}}" for arg in self.args.values()])
        latex_open += "\n"
        latex_body = ""
        for child in self.children:
            latex_child = child.__str__()
            for latex_ch in latex_child.split("\n"):
                latex_body += "\t" + latex_ch + "\n"
        latex_close = f"\\end{{{self.command}}}\n"
        return latex_open + latex_body + latex_close

    def __str__(self):
        return self.to_latex()


class latexCommand:
    def __init__(
        self, command, args=None, opt_args=None, **kwargs,
    ):

        if args is None:
            self.args = {}
        else:
            self.args = args
        if opt_args is None:
            self.opt_args = {}
        else:
            self.opt_args = opt_args
        self.command = command

    def to_latex(self):
        string = f"\\{self.command}"
        string += "".join([f"[{optarg}]" for optarg in self.opt_args.values()])
        args_arr = self.args if isinstance(self.args, list) else self.args.values()
        arg_arr = [f"{{{arg}}}" for arg in args_arr if not arg is None]
        if len(arg_arr) == 0:
            string += "{}"
        else:
            string += "".join(arg_arr)
        return string

    def __str__(self):
        return self.to_latex()


class document(latexEnv):
    def __init__(self, children=None):
        super().__init__(command="document", children=children)


class section(latexCommand):
    def __init__(self, title=None):
        args = {"title": "" if title is None else title}
        super().__init__(command="section", args=args)


class cventry(latexCommand):
    def __init__(
        self,
        year=None,
        job_title=None,
        institution=None,
        city=None,
        grade=None,
        description=None,
    ):
        args = {
            "year": year,
            "job_title": job_title,
            "institution": institution,
            "city": city,
            "grade": grade,
            "description": description,
        }
        for key in args.keys():
            if args[key] is None:
                args[key] = ""
        super().__init__(command="cventry", args=args)


class cvitem(latexCommand):
    def __init__(self, items=None, description=None, **kwargs):
        args = {"items": items, "description": description}
        for key in args.keys():
            if args[key] is None:
                args[key] = ""
        super().__init__(command="cvitem", args=args, **kwargs)


class latexContainer:
    def __init__(self, children=None):
        if children is None:
            self.children = []
        elif not isinstance(children, list):
            self.children = [children]
        else:
            self.children = children

    def to_latex(self):
        latex_string = ""
        for child in self.children:
            latex_string += child.__str__() + "\n"
        return latex_string

    def __str__(self):
        return self.to_latex()


class usepackage(latexCommand):
    def __init__(self, package, **kwargs):
        super().__init__(
            command="usepackage", args={"package": package}, opt_args=kwargs
        )


# sec = section("Hello world")
# cvi = cvitem()
# doc = document(children=[sec])
#
# documentclass = latexCommand(
#    command="documentclass",
#    args={"docclass": "moderncv"},
#    opt_args={"args": "10pt,a4paper,sans"},
# )
# settings = latexContainer(
#    children=[
#        usepackage(package="multicol"),
#        usepackage(package="geometry", scale="scale=0.75"),
#        latexCommand(command="firstname", args={"firstname": ""}),
#        latexCommand(command="familyname", args={"familyname": ""}),
#
#    ]
# )
# container = latexContainer(children=[documentclass, settings, doc])
# main = container.__str__()
# print(main)
# pdfl = PDFLaTeX.from_binarystring(main.encode("utf-8"), jobname="test")
# pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)

