# Manages the Google Sheets side of the script
import gspread
# Manages sending Generic HTTP requests
import requests
# Manages Sleep for pausing between API calls for Scryfall
from time import sleep
# Manages Pandas for easy processing of the sheet data
import pandas as pd
# Authentication File Name
import sys
sys.path.insert(1, '../AuthFile')
import AuthFile
# Global Debug Flag
Debug = True

# Manages all the functionality for updating the sheet, 
# from grabbing the sheet data, to pulling the Scryfall API data,
# To processing the prices, and pushing it back to the sheet; It manages it all.
class UpdateSheet:

    # Manages
    Data = ''
    # Stores the row count 
    Rows = 0
    # Stores a list of the failed requests
    FailedRequests = []

    # Method used to update all the Legends prices
    def UpdateLegendPrices(self,sheet):
        worksheet = sheet.worksheet("Legends")
        self.Run(worksheet)

    # Method used to update all the Planeswalker prices
    def UpdatePlaneswalkerPrices(self,sheet):
        worksheet = sheet.worksheet("Planeswalkers")
        self.Run(worksheet)

    # Method used to update all the Land prices
    def UpdateLandPrices(self,sheet):
        worksheet = sheet.worksheet("Lands")
        self.Run(worksheet)

    # Method used to update all the Green Card prices
    def UpdateGreenPrices(self,sheet):
        worksheet = sheet.worksheet("Green Spells")
        self.Run(worksheet)

    # Method used to update all the Blue Card prices
    def UpdateBluePrices(self,sheet):
        worksheet = sheet.worksheet("Blue Spells")
        self.Run(worksheet)

    # Method used to update all the White Card prices
    def UpdateWhitePrices(self,sheet):
        worksheet = sheet.worksheet("White Spells")
        self.Run(worksheet)
    
    # Method used to update all the Black Card prices
    def UpdateBlackPrices(self,sheet):
        worksheet = sheet.worksheet("Black Spells")
        self.Run(worksheet)

    # Method used to update all the Black Card prices
    def UpdateRedPrices(self,sheet):
        worksheet = sheet.worksheet("Red Spells")
        self.Run(worksheet)

    # Method used to update all the Multicolor Card Prices  
    def UpdateMulticolor(self,sheet):
        worksheet = sheet.worksheet("Multicolor Spells")
        self.Run(worksheet)

    # Method used to update all the Colorless Card prices
    def UpdateColorlessPrices(self,sheet):
        worksheet = sheet.worksheet("Colorless Spells")
        self.Run(worksheet)

    # Method used to update all the Bulk Card prices
    def UpdateBulkPrices(self,sheet):
        worksheet = sheet.worksheet("Bulk")
        self.Run(worksheet)

    # No input
    # Authorize the script to edit the sheet, and open the sheet
    # Return the sheet
    def OpenSheet(self):
        #Authorization
        serviceAccount = gspread.service_account(filename=AuthFile.filename)
        #Open the spreadsheet
        sheet = serviceAccount.open("MTG Library")
        return sheet

    # Takes in the input of the worksheet
    # Uses the Gspread API to grab all the records and uses Pandas to store it in a dataframe
    # No returned value; Sets self.Data to the dataframe 
    def GetWorksheetData(self,worksheet):
        self.Data = pd.DataFrame(worksheet.get_all_records())

    # No Input
    # Gets the length of the dataframe stored in self.Data
    # No Return; Sets self.Rows to be the length of self.Data
    def GetRows(self):
        self.Rows = len(self.Data.index)

    # Take in the a Worksheet
    # For each item in a given worksheet complete all the steps needed to update the data
    # No Return; Last step sends the udpated self.data to the worksheet
    def Run(self,worksheet):
        self.GetWorksheetData(worksheet)
        self.GetRows()
        print(self.Rows)
        row = 0
        # Loop through the rows on the sheet
        while int(row) < int(self.Rows):
            # Generate the url used for the api request
            url = self.GenerateUrl(row)
            # Get the data from the scryfall api as a dictionary
            dict = self.SendRequest(url,row)
            # Get the price for the card from the dictionary
            price = self.GetPrice(row,dict)
            # Get the image URI for the card from the dictionary
            image = self.GetImageLink(row,dict)
            # Sets the previous price col to be the current price
            self.SetPreviousPrice(row)
            # Updates the price col to contain the price obtained from the dict
            self.UpdatePrice(row,price)
            # Set the image uri if the image is an empty string currently
            self.SetImage(row,image)
            # Mandatory 50 - 100 milliesecond wait between scryfall API calls
            sleep(0.1)
            row += 1
        # Update the worksheet with the updated data in self.data
        self.UpdateSheetData(worksheet)

    # Takes in the Name and set of a card
    # Generates the url used to send the scryfall API request
    # Returns the generated url as a string
    def GenerateUrl(self,row):
        if str(self.Data.loc[row,"Collector Number"]) != "":
            url = "https://api.scryfall.com/cards/search?pretty=true&q=in:paper+set:" + self.Data.loc[row,"Set"] + "+" + self.Data.loc[row,"Name"] + "+cn:" + str(self.Data.loc[row,"Collector Number"])
        else:
            url = "https://api.scryfall.com/cards/search?pretty=true&q=in:paper+set:" + self.Data.loc[row,"Set"] + "+" + self.Data.loc[row,"Name"]
        print("Generated URL for '" + self.Data.loc[row,"Name"] + " | " + self.Data.loc[row,"Set"] + "' " + url) 
        return url    

    # Take in the scryfall API request url
    # Grab the dictionary response from that API
    # Return the dictionary response
    def SendRequest(self,url,row):
        retval = ""
        response = requests.get(url)
        retval = response.json()
        # If reponse status is 404
        if retval.get('status') == 404:
            print("THE URL: " + str(url) + " HAS FAILED! CHECK SPELLING!")
            self.FailedRequests.append([row])
            print([row])
            retval = "bad url"
        return retval

    # Takes In a dictionary, and row
    # Grab the image url if there is not currently an image in the record
    # Return the image url
    def GetImageLink(self,row,dict):
        image = ""
        try:
            if(self.Data.loc[row,"Image"] == ""):
                image = dict.get('data',{})[0].get('image_uris').get('normal')
        except:
            print("FAILED TO GET IMAGE FOR " + str(self.Data.loc[row,"Name"]).upper())
        return image

    # Takes in a dictionary, foil and etched
    # Grab the price associated either foil, etched, or non-foil
    # Return the price of the card  
    def GetPrice(self,row,dict):
        price = ""
        if dict != "bad url":
            try:
                if(self.Data.loc[row,"Extra"] == 'FOIL'):
                    price = dict.get('data', {})[0].get('prices').get('usd_foil')
                    if Debug:
                        print("Price: " + price)
                
                elif(self.Data.loc[row,"Extra"] == 'ETCHED'):
                    price = dict.get('data', {})[0].get('prices').get('usd_etched')
                    if Debug:
                        print("Price: " + price)
                
                else:
                    price = dict.get('data', {})[0].get('prices').get('usd')
                    if Debug:
                        print("Price: " + price)
            # If for whatever reason, we are unable to get a price given the input print an error and set price to "" in order to not send bad data    
            except:
                print("FAILED TO GET PRICE FOR " + str(self.Data.loc[row,"Name"]).upper())
                price = ""
        return price

    # Takes in the current row
    # Grabs the value of the current price and sets that to the old price before it gets updated
    # No return; Updates the old price col 
    def SetPreviousPrice(self,row):
        self.Data.loc[row,"Old Price"] = self.Data.loc[row,"Price"]

    # Takes In the row and image
    # Updates the image col to the image uri if empty
    # No return
    def SetImage(self,row,image):
        if self.Data.loc[row,"Image"] == "":
            self.Data.loc[row,"Image"] = image

    # Takes in the current row and the price for that row
    # Updates the price on the given row with the price given
    # No return; 
    def UpdatePrice(self,row,price):
        self.Data.loc[row,"Price"] = price
        # Set the price * quantity col to be the google sheet function used to calculate this value
        self.Data.loc[row,"Price * Quantity"] = '=multiply(B' +str(row +2) + ',G' +str(row + 2) + ')'

    # Takes in the worksheet
    # Uses the Gspread API to update the whole worksheet in one step
    # No return value
    def UpdateSheetData(self,worksheet):
        worksheet.update([self.Data.columns.values.tolist()] + self.Data.values.tolist(),value_input_option="USER_ENTERED")


RunUpdate = UpdateSheet()   
sheet = RunUpdate.OpenSheet() 
RunUpdate.UpdatePlaneswalkerPrices(sheet)
RunUpdate.UpdateLegendPrices(sheet)
RunUpdate.UpdateGreenPrices(sheet)
RunUpdate.UpdateBluePrices(sheet)
RunUpdate.UpdateWhitePrices(sheet)
RunUpdate.UpdateLandPrices(sheet)
RunUpdate.UpdateBulkPrices(sheet)
RunUpdate.UpdateRedPrices(sheet)
RunUpdate.UpdateColorlessPrices(sheet)
RunUpdate.UpdateBlackPrices(sheet)
RunUpdate.UpdateMulticolor(sheet)