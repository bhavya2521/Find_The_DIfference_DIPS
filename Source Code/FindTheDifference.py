import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from skimage.metrics import structural_similarity as ssim
import cv2
import imutils
from PIL import Image

class FindTheDifference:
    def compare(self, image1, image2):
        imageA = cv2.imread(image1)
        imageB = cv2.imread(image2)
        # print(imageA.shape)
        # print(imageB.shape)

        # convert the images to grayscale
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        # compute the Structural Similarity Index (SSIM) between the two
        # images, ensuring that the difference image is returned
        (score, diff) = ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        print("SSIM: {}".format(score))

        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # show the output images
        # cv2.imshow("Original", imageA)
        # cv2.imshow("Modified", imageB)

        cv2.imwrite('Original'+image1, imageA)
        cv2.imwrite('Modified'+image2, imageB)
        img1 = Image.open('Original'+image1)
        img2 = Image.open('Modified'+image2)
        img1.show()
        img2.show()
        # cv2.imshow("Diff", diff)
        # cv2.imshow("Thresh", thresh)
        # cv2.waitKey(10000)

    def button(self):
        image1 = self.Entry1.get()
        image2 = self.Entry2.get()

        if image1 == "":
            messagebox.showerror("Error", "Please enter original image name")
            return

        # Checking for existence of the Original File
        try:
            f = open(image1)
            f.close()
        except IOError:
            messagebox.showerror("Error", "Original Image doesn't exist")
            return

        try:
            imageA = cv2.imread(image1)
            x = imageA.shape
        except AttributeError:
            messagebox.showerror("Error", "Please enter correct Original Image name")
            return

        if image2 == "":
            messagebox.showerror("Error", "Please enter modified image name")
            return

        # Checking for existence of the Modified File
        try:
            f = open(image2)
            f.close()
        except IOError:
            messagebox.showerror("Error", "Modified Image doesn't exist")
            return

        try:
            imageB = cv2.imread(image2)
            y = imageB.shape
        except AttributeError:
            messagebox.showerror("Error", "Please enter correct Modified Image name")
            return

        # Checking for the dimensions of both the Images
        if x != y:
            messagebox.showerror("Error", "Dimensions not matched")
        else:
            self.compare(image1, image2)

    def __init__(self, master=None):
        # build ui
        self.window = ttk.Frame(master)

        # compare button
        self.Compare = ttk.Button(self.window)
        self.Compare.configure(text='Compare', command=self.button)
        self.Compare.grid(column='1', row='7', sticky='s')
        self.Compare.columnconfigure('1', weight='1')

        # Original Image Label
        self.label1 = ttk.Label(self.window)
        self.label1.configure(text='Original Image')
        self.label1.grid(column='0', row='2', sticky='new')
        self.label1.grid_propagate(0)
        self.label1.rowconfigure('0', weight='1')
        self.label1.columnconfigure('0', weight='1')

        # Modified Image Label
        self.label2 = ttk.Label(self.window)
        self.label2.configure(text='Modified Image')
        self.label2.grid(column='0', row='4', sticky='nw')
        self.label2.rowconfigure('2', weight='1')
        self.label2.columnconfigure('0', weight='1')

        # Original Image Text Entry Field
        self.Entry1 = ttk.Entry(self.window)
        self.Entry1.grid(column='2', row='2')
        self.Entry1.rowconfigure('0', weight='1')
        self.Entry1.columnconfigure('1', weight='1')

        # Modified Image Text Entry Field
        self.Entry2 = ttk.Entry(self.window)
        self.Entry2.grid(column='2', row='4')
        self.Entry2.rowconfigure('2', weight='1')
        self.Entry2.columnconfigure('1', weight='1')

        self.frame2 = ttk.Frame(self.window)
        self.frame2.configure(height='200', width='200')
        self.frame2.grid(column='0', row='10', sticky='nsew')
        self.frame2.columnconfigure('0', weight='1')

        # Heading Image
        self.placeholder1 = ttk.Label(self.window)
        self.text_png = t.PhotoImage(file='text.png')
        self.placeholder1.configure(image=self.text_png)
        self.placeholder1.grid(column='1', row='0')

        # padding
        self.placeholder2 = ttk.Label(self.window)
        self.placeholder2.grid(column='0', row='1')

        # padding
        self.placeholder3 = ttk.Label(self.window)
        self.placeholder3.configure(cursor='bottom_left_corner')
        self.placeholder3.grid(column='0', row='3')

        # padding
        self.placeholder4 = ttk.Label(self.window)
        self.placeholder4.grid(column='0', row='5')

        # padding
        self.placeholder5 = ttk.Label(self.window)
        self.placeholder5.grid(column='0', row='6')

        # padding
        self.window.configure(cursor='arrow', height='800', width='800')
        self.window.pack(expand='true', ipadx='100', ipady='200', padx='100', pady='100', side='right')

        # Main widget
        self.mainwindow = self.window

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    import tkinter as t

    root = t.Tk()
    root.title("DIPS Project Group 7")
    image = PhotoImage(file='icon.png')
    root.iconphoto(False, image)
    app = FindTheDifference(root)
    app.run()

