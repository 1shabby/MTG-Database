#manages Google Sheets API
import gspread
#Manages Generic HTTP requests
import requests
#Manages Sleep
from time import sleep
# Authentication File Name
import AuthFile

#Global Debug Flag
Debug = True
class UpdateSheet:
    Calls = 0
    FailedRequests = []
    def UpdateLegendPrices(self,sheet):
        worksheet = sheet.worksheet("Legends")
        self.Run(worksheet)

    def UpdatePlaneswalkerPrices(self,sheet):
        worksheet = sheet.worksheet("Planeswalkers")
        self.Run(worksheet)


    def UpdateLandPrices(self,sheet):
        worksheet = sheet.worksheet("Lands")
        self.Run(worksheet)

    def UpdateGreenPrices(self,sheet):
        worksheet = sheet.worksheet("Green Spells")
        self.Run(worksheet)

    def UpdateBluePrices(self,sheet):
        worksheet = sheet.worksheet("Blue Spells")
        self.Run(worksheet)
    def UpdateWhitePrices(self,sheet):
        worksheet = sheet.worksheet("White Spells")
        self.Run(worksheet)
    
    def UpdateRedPrices(self,sheet):
        worksheet = sheet.worksheet("Red Spells")
        self.Run(worksheet)

    def UpdateBlackPrices(self,sheet):
        worksheet = sheet.worksheet("Black Spells")
        self.Run(worksheet)

    def UpdateColorlessPrices(self,sheet):
        worksheet = sheet.worksheet("Colorless Spells")
        self.Run(worksheet)

    def UpdateBulkPrices(self,sheet):
        worksheet = sheet.worksheet("Bulk")
        self.Run(worksheet)
    # No input
    # Authorize the script to edit the sheet, and open the sheet
    # Return none
    def OpenSheet(self):
        #Authorization
        serviceAccount = gspread.service_account(filename=AuthFile.filename)
        #Open the spreadsheet
        sheet = serviceAccount.open("MTG Library")
        return sheet
    # Take in the scryfall API request url
    # Grab the dictionary response from that API
    # Return the dictionary response
    def SendRequest(self,url,row):
        retval = ""
        response = requests.get(url)
        retval = response.json()
        #If reponse status is 404
        if retval.get('status') == 404:
            print("THE URL: " + str(url) + " HAS FAILED! CHECK SPELLING!")
            broken = [url,row]
            print(broken)
            self.FailedRequests.append(broken)
            retval = "bad url"
        return retval
    # Takes in a dictionary, foil and etched
    # Grab the price associated either foil, etched, or non-foil
    # Return the price of the card  
    def GetPrice(self,dict,foil):
        price = ""
        if dict != "bad url":
            if(foil == 'etched'):
                price = dict.get('data', {})[0].get('prices').get('usd_etched')
            elif(foil == 'foil'):
                price = dict.get('data', {})[0].get('prices').get('usd_foil')
            else:
                price = dict.get('data', {})[0].get('prices').get('usd')
            if Debug:
                print("Price: " + price)
        return price

    # Takes in the Name and set of a card
    # Generates the url used to send the scryfall API request
    # Returns the generated url as a string
    def GenerateUrl(self,name,set,number=""):
        if str(number) != "None":
            url = "https://api.scryfall.com/cards/search?pretty=true&q=in:paper+set:" + set + "+" + name + "+cn:" + number
        else:
            url = "https://api.scryfall.com/cards/search?pretty=true&q=in:paper+set:" + set + "+" + name
        if Debug:
            print("Generated URL for '" + name + " " + set + "': " + url) 
        return url

    def IsFoil(self,row,worksheet):
        retval = ""
        foil = str(worksheet.acell('C'+ str(row)).value)
        self.ManageGoogleCalls()
        etched = str(worksheet.acell('E'+ str(row)).value)
        self.ManageGoogleCalls()
        if foil == "TRUE":
            retval = "foil"
        elif etched == "TRUE":
            retval = "etched"
        else:
            retval = "none"
        return retval

    def ManageGoogleCalls(self):
        if self.Calls == 60:
            print("REACHED 60 CALLS! Waiting 60 SECONDS!")
            sleep(40)
            self.Calls = 1
        else:
            self.Calls += 1
        if Debug:
                print("Google Calls: " + str(self.Calls))

    def GetRow(self):
        row = input("please enter the row to grab")
        return row

    def SetPreviousPrice(self,worksheet,row):
       price =  worksheet.acell('I' + str(row)).value
       self.ManageGoogleCalls()
       worksheet.update('K'+str(row),price)
       self.ManageGoogleCalls()

    def UpdateCell(self,price, row, worksheet):
        if price != "":
            self.ManageGoogleCalls()
            cell = 'I' + str(row)
            worksheet.update(cell,float(price))

    def RowNum(self,worksheet):
        count = int(worksheet.acell('O1').value)
        self.ManageGoogleCalls()
        return count

    def Run(self,worksheet):
        rows = self.RowNum(worksheet)
        row = 69
        while  row < rows :
           
            name = 'A' + str(row)
            set = 'H' + str(row)
            number = 'G' + str(row)

            name = str(worksheet.acell(name).value)
            self.ManageGoogleCalls()
            set = str(worksheet.acell(set).value)
            self.ManageGoogleCalls()
            number = str(worksheet.acell(number).value)
            self.ManageGoogleCalls()

            url = self.GenerateUrl(name,set,number)
            dict = self.SendRequest(url,row)
            foil = self.IsFoil(row,worksheet)
            price = self.GetPrice(dict,foil)
            self.SetPreviousPrice(worksheet,row)
            self.UpdateCell(price,row,worksheet)
            # Mandatory 50 millisecond gap between API requests as per Scryfall's request
            sleep(0.05)
            row += 1
        self.PrintFailed( worksheet)

    def PrintFailed(self,worksheet):
        print("Failed URLS:")
        for i in range(0,len(self.FailedRequests)) :
            print("Url: " + self.FailedRequests[i] + " Row: " + str(self.FailedRequests[i][i]))
        response = input("Once the rows were fixed, press enter...")
        for l in range(0,len(self.FailedRequests)):
            # Rerun each of the rows that were messed up
            name = 'A' + str(self.FailedRequests[l][l])
            set = 'H' + str(self.FailedRequests[l][l])
            number = 'G' + str(self.FailedRequests[l][l])

            name = str(worksheet.acell(name).value)
            self.ManageGoogleCalls()
            set = str(worksheet.acell(set).value)
            self.ManageGoogleCalls()
            number = str(worksheet.acell(number).value)
            self.ManageGoogleCalls()
            url = self.GenerateUrl(name,set,number)
            self.SendRequest(url,self.FailedRequests[l][l])


RunUpdate = UpdateSheet()   
RunUpdate.Calls = 0
sheet = RunUpdate.OpenSheet() 
# RunUpdate.UpdatePlaneswalkerPrices(sheet)
# RunUpdate.UpdateLegendPrices(sheet)
# RunUpdate.UpdateGreenPrices(sheet)
RunUpdate.UpdateBluePrices(sheet)
#RunUpdate.UpdateLandPrices(sheet)