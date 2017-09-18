import tkinter as tk

class processInput:
    def __init__(self, process_type_in, process_list_in,finalize_process):
        self.process_type = process_type_in
        self.process_list = process_list_in
        dummy_process = self.process_type()
        self.finalize_process = finalize_process

        self.window = tk.Toplevel(width=400)
        self.frame_main = tk.Frame(self.window)
        self.frame_main.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # initialize boundary condition list
        self.Bc_List = []

        tk.Label(self.frame_main, text=dummy_process.getProcessName(), justify=tk.LEFT,
                 relief=tk.GROOVE, padx=70, bg="#606060").grid(row=0, column=0, columnspan=5,
                                                               sticky=tk.W + tk.E)

        self.Node_Label1 = tk.Label(self.frame_main, text="#node", relief=tk.SUNKEN)
        self.Node_Label1.grid(row=1, column=0, columnspan=2,
                              sticky=tk.W + tk.E)

        # check buttons
        is_fixed_ux = tk.BooleanVar()
        CB_node1 = tk.Checkbutton(self.frame_main, text="X",
                                  variable=is_fixed_ux, offvalue=False, onvalue=True)
        CB_node1.grid(row=1, column=2, columnspan=1)

        is_fixed_uy = tk.BooleanVar()
        CB_node2 = tk.Checkbutton(self.frame_main, text="Y",
                                  variable=is_fixed_uy, offvalue=False, onvalue=True)
        CB_node2.grid(row=1, column=3, columnspan=1)

        # entry fields

        [nr_node, u_x, u_y] = [tk.IntVar(), tk.DoubleVar(), tk.DoubleVar()]
        tk.Entry(self.frame_main, width=7, textvariable=nr_node).grid(
            column=0, row=2, columnspan=2, sticky=tk.W + tk.E)
        tk.Entry(self.frame_main, width=7, textvariable=u_x).grid(
            column=2, row=2, sticky=tk.W + tk.E)
        tk.Entry(self.frame_main, width=7, textvariable=u_y).grid(
            column=3, row=2, sticky=tk.W + tk.E)

        ##add button
        label_string = "add boundary cond."
        button_add = tk.Button(self.frame_main, text=label_string, width=14,
                               command=lambda: self.validateAndAddProcess(nr_node, u_x, u_y,is_fixed_ux, is_fixed_uy))
        button_add.grid(row=2, column=4, columnspan=1, sticky=tk.W + tk.E + tk.N + tk.S)

        ##add list
        self.listbox = tk.Listbox(self.frame_main, width=70)
        self.listbox.grid(row=3, column=0, columnspan=5)
        for i in range(len(self.process_list)):
            output_string = self.process_list[i].getProcessInfo()
            self.listbox.insert(tk.END, output_string)

        ##add button
        label_string = "save + close"
        button_add = tk.Button(self.frame_main, text=label_string, width=14,
                               command=lambda: self.closePopup())
        button_add.grid(row=5, columnspan=5, sticky=tk.W + tk.E + tk.N + tk.S)

    def closePopup(self):
        self.window.destroy()
        self.finalize_process()

    def validateAndAddProcess(self,nr_node, u_x, u_y,is_fixed_ux, is_fixed_uy):
        process_vector = [None,None,0]
        if bool(is_fixed_ux.get()):
            process_vector[0] = float(u_x.get())
        if bool(is_fixed_uy.get()):
            process_vector[1] = float(u_y.get())
        new_process = self.process_type()
        node_number = int(nr_node.get())
        new_process.setProcess(node_number,process_vector)
        self.process_list.append(new_process)

        ##add list
        self.listbox = tk.Listbox(self.frame_main, width=70)
        self.listbox.grid(row=3, column=0, columnspan=5)
        for i in range(len(self.process_list)):
            output_string = self.process_list[i].getProcessString()
            self.listbox.insert(tk.END, output_string)

