import cloudscraper as cs #for web scraping and getting data

#ur bloxflip auth so we can get ur game history
auth = ''

scraper = cs.create_scraper() #make a scraper for scraping the data cloud scraper cool and sorta bypass cloudflare

def main():

    r = scraper.get('https://api.bloxflip.com/games/mines/history', headers={"x-auth-token": auth}, params={ 'size': '1','page': '0',}  ) #send a get requests to the api to get info
    
    print(r.json()) #all the information the api has u can get more by increasing the size and page 
    
    uuid = (r.json()['data'][0]['uuid']) #get jus the uuid (round_id) from the page
    print(f"Most Recent uuid: {uuid}") #you can use this to make a uuid verifier if you have the users auth

    mines_location = (r.json()['data'][0]['mineLocations']) #most recent mines location, we will use this to make a guess or a "prediction"
    print(f"Most Recent mine locations: {mines_location}") #print the most recent games mine locations

    clicked_spots = (r.json()['data'][0]['uncoveredLocations']) #most recent spots you clicked in yourt last game
    print(f"Most Recent mine locations: {clicked_spots}") #print the last spot u clicked in ur last game

    grid = ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'] #make a 5x5 (25 total) grid

    for x in mines_location: #make each bomb postion show up on grid
        grid[x] = 'X' #change the bomb posititons to differnt character

    for x in clicked_spots: #loop through every time u clicked and make it convert to grid
        grid[x] = 'O' #change the clicked positions to differnt character

    print("\nLast game played")
    print(grid[0],grid[1],grid[2],grid[3],grid[4] + "\n" + grid[5],grid[6],grid[7],grid[8],grid[9] + "\n" + grid[10],grid[11],grid[12],grid[13],grid[14] + \
        "\n" + grid[15],grid[16],grid[17],grid[18],grid[19] + "\n" + grid[20],grid[21],grid[22],grid[23],grid[24]) #print the grid with the bomb locations

    grid = ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'] #redefine grid so it resets

    roundId = int(''.join(filter(str.isdigit, uuid))) #get only numbers from round id, u could also use this to make a round id verifier

    roundNum = int(str(roundId)[:2]) #get the first two numbers out of the round id
    grid[int(roundNum / 4)] = 'O' #change it to O to know where to click
    grid[int(roundNum / 5)] = 'O' #change it to O to know where to click
    grid[int(roundNum / 7)] = 'O' #change it to O to know where to click

    print("\nPrediction (use the same mine amount as your last game)") #tell user to use same mine amount as last game
    print(grid[0],grid[1],grid[2],grid[3],grid[4] + "\n" + grid[5],grid[6],grid[7],grid[8],grid[9] + "\n" + grid[10],grid[11],grid[12],grid[13],grid[14] + \
        "\n" + grid[15],grid[16],grid[17],grid[18],grid[19] + "\n" + grid[20],grid[21],grid[22],grid[23],grid[24]) #print the prediction

if __name__ == "__main__":
    main()
