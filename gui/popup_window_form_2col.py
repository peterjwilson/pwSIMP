import tkinter as tk

class popup_2_col:
    def __init__(self,number_of_rows,text_vector,title_text,input_variable_vector,finalize_function):
        self.window = tk.Toplevel(width = 400)
        frame_main = tk.Frame(self.window)
        frame_main.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        tk.Label(frame_main, text=title_text, justify=tk.LEFT,
                 relief=tk.GROOVE, padx=20, bg="#606060").grid(row=0, column=0, columnspan=2,
                                                               sticky=tk.W + tk.E)

        for i in range(len(text_vector)):
            tk.Label(frame_main, text=text_vector[i], justify=tk.LEFT,
                     relief=tk.GROOVE, padx=20).grid(row=i+1, column=0,
                                                     sticky=tk.W + tk.E)
            input_variable_vector.append(tk.DoubleVar())
            tk.Entry(frame_main, width=7, textvariable=input_variable_vector[i]).grid(
                column=1, row=i+1, sticky=tk.W + tk.E)

        ##close button
        label_string = "Save and close"
        button_geo = tk.Button(frame_main,text=label_string, width = 14,
         command=lambda: self.closePopup(finalize_function))
        button_geo.grid(row=len(text_vector)+1, column=0, columnspan=2,sticky=tk.W+tk.E+tk.N+tk.S)

    def closePopup(self,finalize_function):
        self.window.destroy()
        finalize_function()