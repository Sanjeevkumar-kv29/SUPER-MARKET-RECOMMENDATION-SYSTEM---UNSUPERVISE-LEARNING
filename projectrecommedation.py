import sys
from datetime import datetime
import tkinter as tk
from tkinter import  *
from tkinter import messagebox
import projectrecommedation_support
import pandas as pd
import os
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    projectrecommedation_support.set_Tk_var()
    top = recommedation (root)
    projectrecommedation_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    projectrecommedation_support.set_Tk_var()
    top = recommedation (w)
    projectrecommedation_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class recommedation:

    nw = datetime.now()


    def __init__(self, top=None):

        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("1053x779+407+166")
        top.minsize(148, 1)
        top.maxsize(1924, 1055)
        top.resizable(1, 1)
        top.title("New Toplevel")
        top.configure(background="#00eeee")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        global releyposition
        x=[]
        totamount = []
        prodlist = []
        pricelist = []
        quantitylist =[]


        def getdata():

            Name = self.name.get()
            Mobile = self.mobile.get()
            prod = self.product.get()
            Quantity = self.quantity.get()
            return Name,Mobile,prod,Quantity


        def add():

            releyposition = 0.310 + 0.05 * len(x)


            name,mobile,prod,quan = getdata()
            if (name and mobile) =='' :
                messagebox._show('ALERT !!','ENTER VALID NAME AND MAILID',icon='error')
            else:

                pricedata = pd.read_csv('price_list.csv')
                price = 0.0
                pricedata = pricedata.values.tolist()
                for item in pricedata:
                    if prod in item:
                        price = float(item[1])

                if price==0.0:
                    messagebox.showerror('ERROR','ENTER VALID ITEM')
                elif quan=='':
                    messagebox.showerror('ERROR', 'ENTER VALID QUANTITY ')
                else:
                    pricelist.append(price)

                    quan=int(quan)
                    prodlist.append(prod)
                    quantitylist.append(quan)
                    totamount.append(price*quan)

                    self.product = tk.Entry(top)
                    self.price = tk.Label(top)
                    self.quantity = tk.Entry(top)
                    self.amount = tk.Label(top)
                    self.grandamount = tk.Label(top)
                    self.product.place(relx=0.037, rely=releyposition,height=25, relwidth=0.175)
                    self.price.place(relx=0.625, rely=0.257+0.05*len(x), height=25, relwidth=0.090)
                    self.quantity.place(relx=0.250, rely=releyposition, height=25, relwidth=0.184)
                    self.amount.place(relx=0.730, rely=0.257+0.05*len(x), height=25, relwidth=0.104)
                    self.amount.configure(text=str(price*quan))
                    self.price.configure(text=str(price))
                    self.grandamount.place(relx=0.852, rely=0.257, height=30, relwidth=0.104)
                    self.grandamount.configure(text=str(sum(totamount)))


                    x.append(1)



        def submit():
            name,mobile,r,r = getdata()
            strprod = prodlist[0]

            for i in range(1,len(prodlist)):
                strprod=strprod+','+prodlist[i]


            df = pd.read_csv('database.csv')
            newdf = pd.DataFrame({'NAME':[name],
                                  'MOBILE':[mobile],
                                  'PRODUCT':[strprod],
                                  'TIME':[str(datetime.now().strftime('%H-%M'))],
                                  'DATE':[str(datetime.now().strftime('%d-%b-%Y'))],
                                  'TOTALAMOUNT':[str(sum(totamount))]})
            ndf=[df,newdf]
            result = pd.concat(ndf)
            result.to_csv('database.csv',index=False)
            messagebox._show('SUCCESS ','submitted sucessfully THANKS FOR SHOPPING')


        def printbill():

            messagebox.askokcancel('PERMISSION', 'DO YOU REALLY WANT TO PRINT ',)
            name, email,r,r=getdata()
            time = datetime.now().strftime('%d-%b-%Y')
            prod=prodlist
            price=pricelist

            pricestr = []
            for x in range(len(prod)):
                pricestr.append(str(price[x]))

            f = open('bill.txt', 'w+')
            f.write('\n\n\n COUSTOMER NAME - ' + name + '                ')
            f.write('EMAIL ID - ' + email + '               ')
            f.write('DATE - ' + time)
            f.write(
                '\n\n\n-----------------------------------------------------YOUR BILL----------------------------------------------------------')

            f.write('\n\n                                     S.no.            PRODUCT            PRICE \n\n')
            for i in range(len(prod)):
                f.write('                                      ' + str(i + 1) + '                ' + prod[i] + ' ' * (
                    23 - len(prod[i]) - 4 if len(prod[i]) > 1 else 18) + pricestr[i] + '\n')

            f.write(
                '\n\n--------------------------------------------------------------------------------------------------------------------------')

            f.write(
                '\n\n                                                                                            GRAND TOTAL -' + str(sum(price)))

            os.startfile("bill.txt", "print")  # print bill using printer

        def recommend():
            dataset = []
            data = pd.read_csv('database.csv')
            data = data['PRODUCT']

            for i in range(len(data)):
                dataset.append(data[i].split(","))

            te = TransactionEncoder()
            transarry = te.fit(dataset).transform(dataset)
            df = pd.DataFrame(transarry, columns=te.columns_)

            apriorimodel = apriori(df, min_support=0.02, use_colnames=True)
            apriorimodel['length'] = apriorimodel['itemsets'].apply(lambda x: len(x))
            itemset = apriorimodel[(apriorimodel['length'] >= 2) & (apriorimodel['support'] >= 0.05)]

            recommenditem = itemset['itemsets']  # return pandas series

            recommenditem = recommenditem.tolist()  # converting series into list


            for i in range(len(recommenditem)):
                recommenditem[i] = list(recommenditem[i])
            recommendvalue =[]

            for x in recommenditem:
                for y in prodlist :
                    if y in x:
                        recommendvalue.append(x)

            print(recommendvalue)
            pricesum=[]
            pricedata = pd.read_csv('price_list.csv')
            price = 0.0
            pricedata = pricedata.values.tolist()
            for prod in recommendvalue:
                for item in pricedata:
                    for i in range(len(prod)):
                        if prod[i] in item:
                            price = float(item[1]) + price
                pricesum.append(price)
                price=0.0

            recommendwindow = Tk()
            recommendwindow.title('RECOMMEND ITEMS')
            recommendwindow.geometry('500x500')
            recommendwindow.maxsize(width=750,height=750)

            for i in range(len(recommendvalue)):
                lab = Label(recommendwindow,text=[str(i+1)]+recommendvalue[i]+[' OFFER!!!!  10% off in recommended items EFFECTIVE PRICE IS  -  '+str(pricesum[i]-pricesum[i]*10/100)])
                lab.grid(column=1,row=i+10)


        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.028, rely=0.039, height=36, width=64)
        self.Label1.configure(activebackground="#00eeee")
        self.Label1.configure(activeforeground="#400080")
        self.Label1.configure(background="#00eeee")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font="-family {Segoe UI} -size 11 -weight bold -slant roman -underline 0 -overstrike 0")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#008080")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''NAME''')

        self.name = tk.Entry(top)
        self.name.place(relx=0.104, rely=0.039,height=34, relwidth=0.137)
        self.name.configure(background="white")
        self.name.configure(disabledforeground="#a3a3a3")
        self.name.configure(font="TkFixedFont")
        self.name.configure(foreground="#000000")
        self.name.configure(highlightbackground="#d9d9d9")
        self.name.configure(highlightcolor="black")
        self.name.configure(insertbackground="black")
        self.name.configure(selectbackground="#c4c4c4")
        self.name.configure(selectforeground="black")
        self.name.configure(textvariable=projectrecommedation_support.name)

        self.Label1_1 = tk.Label(top)
        self.Label1_1.place(relx=0.332, rely=0.039, height=36, width=134)
        self.Label1_1.configure(activebackground="#00eeee")
        self.Label1_1.configure(activeforeground="#400080")
        self.Label1_1.configure(background="#00eeee")
        self.Label1_1.configure(disabledforeground="#a3a3a3")
        self.Label1_1.configure(font="-family {Segoe UI} -size 11 -weight bold -slant roman -underline 0 -overstrike 0")
        self.Label1_1.configure(foreground="#000000")
        self.Label1_1.configure(highlightbackground="#008080")
        self.Label1_1.configure(highlightcolor="black")
        self.Label1_1.configure(text='''EMAIL ID -''')

        self.mobile = tk.Entry(top)
        self.mobile.place(relx=0.465, rely=0.039,height=34, relwidth=0.137)
        self.mobile.configure(background="white")
        self.mobile.configure(disabledforeground="#a3a3a3")
        self.mobile.configure(font="TkFixedFont")
        self.mobile.configure(foreground="#000000")
        self.mobile.configure(highlightbackground="#d9d9d9")
        self.mobile.configure(highlightcolor="black")
        self.mobile.configure(insertbackground="black")
        self.mobile.configure(selectbackground="#c4c4c4")
        self.mobile.configure(selectforeground="black")
        self.mobile.configure(textvariable=projectrecommedation_support.mobile)

        self.Label1_3 = tk.Label(top)
        self.Label1_3.place(relx=0.066, rely=0.221, height=26, width=115)
        self.Label1_3.configure(activebackground="#00eeee")
        self.Label1_3.configure(activeforeground="#400080")
        self.Label1_3.configure(background="#00eeee")
        self.Label1_3.configure(disabledforeground="#a3a3a3")
        self.Label1_3.configure(font="-family {Segoe UI} -size 11 -weight bold -slant roman -underline 0 -overstrike 0")
        self.Label1_3.configure(foreground="#000000")
        self.Label1_3.configure(highlightbackground="#008080")
        self.Label1_3.configure(highlightcolor="black")
        self.Label1_3.configure(text='''PRODUCT''')

        self.Label1_4 = tk.Label(top)
        self.Label1_4.place(relx=0.600, rely=0.212, height=25, width=150)
        self.Label1_4.configure(activebackground="#00eeee")
        self.Label1_4.configure(activeforeground="#400080")
        self.Label1_4.configure(background="#00eeee")
        self.Label1_4.configure(disabledforeground="#a3a3a3")
        self.Label1_4.configure(font="-family {Segoe UI} -size 11 -weight bold -slant roman -underline 0 -overstrike 0")
        self.Label1_4.configure(foreground="#000000")
        self.Label1_4.configure(highlightbackground="#008080")
        self.Label1_4.configure(highlightcolor="black")
        self.Label1_4.configure(text='PRICE/UNIT')

        self.Label1_5 = tk.Label(top)
        self.Label1_5.place(relx=0.735, rely=0.212, height=25, relwidth=0.095)
        self.Label1_5.configure(activebackground="#00eeee")
        self.Label1_5.configure(activeforeground="#400080")
        self.Label1_5.configure(background="#00eeee")
        self.Label1_5.configure(disabledforeground="#a3a3a3")
        self.Label1_5.configure(font="-family {Segoe UI} -size 11 -weight bold -slant roman -underline 0 -overstrike 0")
        self.Label1_5.configure(foreground="#000000")
        self.Label1_5.configure(highlightbackground="#008080")
        self.Label1_5.configure(highlightcolor="black")
        self.Label1_5.configure(text='''AMOUNT''')


        self.Label1_6 = tk.Label(top)
        self.Label1_6.place(relx=0.28, rely=0.218, height=26, relwidth=0.112)
        self.Label1_6.configure(activebackground="#00eeee")
        self.Label1_6.configure(activeforeground="#400080")
        self.Label1_6.configure(background="#00eeee")
        self.Label1_6.configure(disabledforeground="#a3a3a3")
        self.Label1_6.configure(font="-family {Segoe UI} -size 11 -weight bold -slant roman -underline 0 -overstrike 0")
        self.Label1_6.configure(foreground="#000000")
        self.Label1_6.configure(highlightbackground="#008080")
        self.Label1_6.configure(highlightcolor="black")
        self.Label1_6.configure(text='''QUANTITY''')

        self.Label1_7 = tk.Label(top)
        self.Label1_7.place(relx=0.828, rely=0.212, height=25, relwidth=0.150)
        self.Label1_7.configure(activebackground="#00eeee")
        self.Label1_7.configure(activeforeground="#400080")
        self.Label1_7.configure(background="#00eeee")
        self.Label1_7.configure(disabledforeground="#a3a3a3")
        self.Label1_7.configure(font="-family {Segoe UI} -size 11 -weight bold -slant roman -underline 0 -overstrike 0")
        self.Label1_7.configure(foreground="#000000")
        self.Label1_7.configure(highlightbackground="#008080")
        self.Label1_7.configure(highlightcolor="black")
        self.Label1_7.configure(text='''GRAND TOTAL''')

        self.product = tk.Entry(top)
        self.product.place(relx=0.037, rely=0.257,height=25, relwidth=0.175)
        self.product.configure(background="white")
        self.product.configure(disabledforeground="#a3a3a3")
        self.product.configure(font="TkFixedFont")
        self.product.configure(foreground="#000000")
        self.product.configure(highlightbackground="#d9d9d9")
        self.product.configure(highlightcolor="black")
        self.product.configure(insertbackground="black")
        self.product.configure(selectbackground="#c4c4c4")
        self.product.configure(selectforeground="black")
        self.product.configure(textvariable=projectrecommedation_support.product)

        '''self.price = tk.Entry(top)
        self.price.place(relx=0.23, rely=0.257,height=25, relwidth=0.184)
        self.price.configure(background="white")
        self.price.configure(disabledforeground="#a3a3a3")
        self.price.configure(font="TkFixedFont")
        self.price.configure(foreground="#000000")
        self.price.configure(highlightbackground="#d9d9d9")
        self.price.configure(highlightcolor="black")
        self.price.configure(insertbackground="black")
        self.price.configure(selectbackground="#c4c4c4")
        self.price.configure(selectforeground="black")
        self.price.configure(textvariable=projectrecommedation_support.price)'''

        self.quantity = tk.Entry(top)
        self.quantity.place(relx=0.250, rely=0.257,height=25, relwidth=0.184)
        self.quantity.configure(background="white")
        self.quantity.configure(disabledforeground="#a3a3a3")
        self.quantity.configure(font="TkFixedFont")
        self.quantity.configure(foreground="#000000")
        self.quantity.configure(highlightbackground="#d9d9d9")
        self.quantity.configure(highlightcolor="black")
        self.quantity.configure(insertbackground="black")
        self.quantity.configure(selectbackground="#c4c4c4")
        self.quantity.configure(selectforeground="black")
        self.quantity.configure(textvariable=projectrecommedation_support.quantity)

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.057, rely=0.895, height=53, relwidth=0.166)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#99CCFF")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''ADD+''')
        self.Button1.configure(command=add)

        self.Button1_4 = tk.Button(top)
        self.Button1_4.place(relx=0.236, rely=0.893, height=53, relwidth=0.166)
        self.Button1_4.configure(activebackground="#ececec")
        self.Button1_4.configure(activeforeground="#000000")
        self.Button1_4.configure(background="#99CCFF")
        self.Button1_4.configure(disabledforeground="#a3a3a3")
        self.Button1_4.configure(foreground="#000000")
        self.Button1_4.configure(highlightbackground="#d9d9d9")
        self.Button1_4.configure(highlightcolor="black")
        self.Button1_4.configure(pady="0")
        self.Button1_4.configure(text='''SUBMIT''')
        self.Button1_4.configure(command=submit)

        self.Button1_5 = tk.Button(top)
        self.Button1_5.place(relx=0.627, rely=0.89, height=53, relwidth=0.176)
        self.Button1_5.configure(activebackground="#ececec")
        self.Button1_5.configure(activeforeground="#000000")
        self.Button1_5.configure(background="#99CCFF")
        self.Button1_5.configure(disabledforeground="#a3a3a3")
        self.Button1_5.configure(foreground="#000000")
        self.Button1_5.configure(highlightbackground="#d9d9d9")
        self.Button1_5.configure(highlightcolor="black")
        self.Button1_5.configure(pady="0")
        self.Button1_5.configure(text='''PRINT BILL''')
        self.Button1_5.configure(command=printbill)

        self.Button1_6 = tk.Button(top)
        self.Button1_6.place(relx=0.818, rely=0.888, height=53, relwidth=0.156)
        self.Button1_6.configure(activebackground="#ececec")
        self.Button1_6.configure(activeforeground="#000000")
        self.Button1_6.configure(background="#99CCFF")
        self.Button1_6.configure(disabledforeground="#a3a3a3")
        self.Button1_6.configure(foreground="#000000")
        self.Button1_6.configure(highlightbackground="#d9d9d9")
        self.Button1_6.configure(highlightcolor="black")
        self.Button1_6.configure(pady="0")
        self.Button1_6.configure(text='''RECOMMEND''')
        self.Button1_6.configure(command=recommend)


        self.time = tk.Label(top)
        self.time.place(relx=0.75, rely=0.039, height=35, relwidth=0.210)
        self.time.configure(activebackground="#00eeee")
        self.time.configure(activeforeground="black")
        self.time.configure(background="#00eeee")
        self.time.configure(disabledforeground="#a3a3a3")
        self.time.configure(foreground="#000000")
        self.time.configure(highlightbackground="#d9d9d9")
        self.time.configure(highlightcolor="black")
        self.time.configure(text=datetime.now().strftime('%d-%b-%Y'))

        self.amount = tk.Label(top)
        self.amount.place(relx=0.730, rely=0.257, height=25, relwidth=0.102)
        self.amount.configure(activebackground="#00eeee")
        self.amount.configure(activeforeground="black")
        self.amount.configure(background="#00eeee")
        self.amount.configure(disabledforeground="#a3a3a3")
        self.amount.configure(foreground="#000000")
        self.amount.configure(highlightbackground="#d9d9d9")
        self.amount.configure(highlightcolor="black")


        self.grandamount = tk.Label(top)
        self.grandamount.place(relx=0.852, rely=0.257, height=25, relwidth=0.104)
        self.grandamount.configure(activebackground="#00eeee")
        self.grandamount.configure(activeforeground="black")
        self.grandamount.configure(background="#00eeee")
        self.grandamount.configure(disabledforeground="#a3a3a3")
        self.grandamount.configure(foreground="#000000")
        self.grandamount.configure(highlightbackground="#d9d9d9")
        self.grandamount.configure(highlightcolor="black")


if __name__ == '__main__':
    vp_start_gui()





