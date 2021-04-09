from src.cliFunctionality.helpMenu import helpMenu
from src.cliFunctionality.openPorts import openPorts


# MAIN EVENT LOOP
def mainLoop(history) -> None:
    usrInput = ''
    terminate = False

    while (not terminate):
        usrInput = str(input('> '))
        # CASE: Break in event of a 'q' or 'Q' entered
        if usrInput.lower() == 'q':
            terminate = True
            continue
        
        # Add most recent input to history queue

        if usrInput == '':
            mostRecent = history.get_recents()
            if len(mostRecent) == 0:
                print("You must enter a command")
                continue

            st = ''
            for idx, val in enumerate(mostRecent):
                st += f"{idx + 1}: {val}\n"

            prompt = "Enter the corresponding number: "

            print(st)
            choice = int(input(prompt))

            handleFlag(parseInput(mostRecent[choice - 1]), history)
        
        else:
            history.update(usrInput)

            handleFlag(parseInput(usrInput), history)
    return

def getFlags() -> dict:
    return {
        'h': helpMenu,
        'help': helpMenu,
        'o': openPorts
    }


# PARSE THE INPUT, ERROR CHECKING, and TOKENIZE INTO FLAG(S)
def parseInput(usrInput: str) -> str:
    tokens = usrInput.split(' ')
    flags = getFlags()
    
    # ERROR CASES
    if len(tokens) == 0:
        handleError('nc')
        return

    if tokens[0].upper() != 'MLH':
        handleError('cnf')
        return
    
    if tokens[1][0] != '-':
        handleError('nf')
        return

    tokens[1] = tokens[1].strip('-')

    if not tokens[1] in flags:
        handleError('fnf')
        return
    
    # error handle (future): unkown command
    return (tokens[1:])

# HANDLE THE FLAGS PASSED IN
def handleFlag(command: str, history) -> None:
    # Seperate flag from options
    options = command[1:]
    type = command[0]
    # Retreive flags from function above
    flags = getFlags()

    flags[type](options, history)


# ERROR HANDLING
def handleError(type: str) -> None:
    # CASES 
    def invalid_caf():
        print("Invalid Inpt: Character(s) found after command")

    def invalid_cnf():
        print("Invalid Input: Prefix command is something other than 'MLH'")

    def invalid_nc():
        print("Invalid Input: No characters found")

    def invalid_nf():
        print("Invalid Input: No flag found")

    def invalid_fne():
        print("Invalid Input: Flag does not exist")

    # HANDLING CASES
    options = {
        'caf' : invalid_caf,
        'caf' : invalid_caf,
        'cn' : invalid_nc,
        'nf' : invalid_nf,
        'fne' : invalid_fne
    }

    # CASE TO CATCH UNHANDLED ERROR -> TO BE CHANGED LATER
    if not type in options:
        print("Invalid Input: Unknown Error")
    else:
        options[type]()