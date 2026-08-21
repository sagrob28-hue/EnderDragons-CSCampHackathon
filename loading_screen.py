import colorsys
from time import sleep
from ansi import Ansi, IOUtils
from sys import stdout

m, b, r = Ansi.fg(127), Ansi.BLUE, Ansi.RED
M, R = Ansi.BG_BRIGHT_MAGENTA, Ansi.BG_DEFAULT

class LoadingScreen:

    TITLE_STR = (Ansi.BLUE + Ansi.BOLD
+ f"""
 ______   ___   _______  _______  __    _  _______  _______  ___   _______        _______  __   __     {r}#{b}
|      | |   | |   _   ||       ||  |  | ||       ||       ||   | |       |      |       ||  | |  |    {r}#{b}
|  _    ||   | |  |_|  ||    ___||   |_| ||   _   ||  _____||   | |  _____|      |    _  ||  |_|  | {r}#######{b}
| | |   ||   | |       ||   | __ |       ||  | |  || |_____ |   | | |_____       |   |_| ||       |    {r}#{b}
| |_|   ||   | |       ||   ||  ||  _    ||  |_|  ||_____  ||   | |_____  | ___  |    ___||_     _|    {r}#{b}
|       ||   | |   _   ||   |_| || | |   ||       | _____| ||   |  _____| ||   | |   |      |   |  
|______| |___| |__| |__||_______||_|  |__||_______||_______||___| |_______||___| |___|      |___|
By: Team Ender Dragons"""
+ Ansi.RESET
                 )

    # source: https://patorjk.com/software/taag/#p=display&f=Modular&t=diagnosis.py&x=none&v=4&h=4&w=80&we=false

    BRAIN = (m +
f"""
      {M}_---~~(~~-_.{R}       
    {M}_(        )   ){R}      A program that diagnoses your symptoms!
  {M},   ) -~~- ( ,-' )_{R}    (Don't take this as serious medical advice.)
 {M}(  `-,_..`., )-- '_,){R}   Learn more about all kinds of diseases and
{M}( ` _)  (  -~( -_ `,  |{R}  their symptoms!
{M}(_-  _  ~_-~~~~`,  ,' ){R}  
  {M}`~ -^(    __;-,((())){R}  Built entirely in Python 3.
        {M}~~~~ (_ -_(()){R}   Good luck!
               {M}`\\  ]{R}
                 {M}[_]{R}"""
    )

    # source: https://www.asciiart.eu/people/body-parts/brains
    # edited to remove brackets

    @staticmethod
    def rainbow_iter(character: str="#", length: int=60, sat: float=0.6, val: float=1.0):

        for i in range(length):
            r, g, b = (int(c * 255) for c in colorsys.hsv_to_rgb(i / length, sat, val))

            yield f"\033[38;2;{r};{g};{b}m{character}"

    @staticmethod
    def load():

        IOUtils.clear()

        for line in LoadingScreen.TITLE_STR.splitlines():
            stdout.write(line + "\n")
            stdout.flush()
            sleep(0.05)

        sleep(2)

        IOUtils.clear()

        stdout.write(LoadingScreen.BRAIN)
        stdout.flush()

        for character in LoadingScreen.rainbow_iter():
            stdout.write(character)
            stdout.flush()
            sleep(0.02)

        sleep(5)

        stdout.write(Ansi.RESET)
        IOUtils.clear()

        sleep(2)
