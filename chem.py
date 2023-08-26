import pandas as pd
from typing import Union

class Chem:
    def __init__(self):
        self.AVOGADRO = 6.022e23;
        self.elements_df = self.init_elements_df()

    def __calculate_compound_molarmass(self, compound: str, i: int, sum_: float) -> float:
    """Calculates molar_mass of compound"""

        if i < len(compound):
            # Get name of next element
            elementBuffer = ""
            while i < len(compound) and compound[i].isalpha():
                elementBuffer += compound[i]
                i += 1

            if len(elementBuffer) == 0:
                raise ValueError("\n::NO SUCH ELEMENT:: -> CHEM.__calculate_compound_molarmass")

            # Get number of atoms
            atom_count_buffer = ""
            while i < len(compound) and compound[i].isdigit():
                # First read the number of atoms into a string
                atom_count_buffer += compound[i]
                i += 1

            if len(atom_count_buffer) == 0:
                raise ValueError(
                    "\n::YOU MUST ENTER THE NUMBER OF ATOMS, EVEN IF THERE IS ONE (eg : 'H2O1'):: -> CHEM.__calculate_compound_molarmass")

            atom_count = int(atom_count_buffer)
            molarmass = self.get_element_molarmass(elementBuffer)

            # Adds the contribution of the molecule to the total molar mass of the compound
            sum_ += (atom_count * molarmass)

            # Recursively calls itself with the new index for compound to read the next molecule
            return self.__calculate_compound_molarmass(compound, i, sum_)

        return sum_

    # Initializes the data frame
    def init_elements_df(self):
        try:
            df = pd.read_csv("./data.csv")
            return df
        except FileNotFoundError:
            raise FileNotFoundError("::failed to load data:: -> the file is missing.")
        except Exception as e:
            raise Exception(f"::failed to load data:: --> {e}")

    # Converts fahrenheit to celsius
    def fahr_to_c(self, f: Union[int, float]) -> float:
        """
        chem = Chem()
        chem.fahr_to_c(32.0) # returns 0.0
        """

        return (f - 32.0) / 1.8

    # Converts celsius to fahrenheit
    def c_to_fahr(self, c: Union[int, float]) -> float:
        """
        chem = Chem()
        chem.c_to_fahr(0): # returns 32.0
        """

        return (c * 9.0 / 5.0) + 32.0
    
    # Returns the atomic number based on the element symbol or name
    def get_atomic_number(self, element: str) -> float:
        """
        chem = Chem()
        chem.get_atomic_number('He') # returns 2
        chem.get_atomic_number('Lithium') # returns 3
        """

        field = "element" if len(element) <= 2 else "name"

        if element not in self.elements_df[field].values:# Check for argument
            raise ValueError(f"\n::NO SUCH {field}:: -> CHEM.get_atomic_number")

        atomic_number = self.elements_df[self.elements_df[field] == element]["AtomicNumber"].values[0]

        if pd.isna(atomic_number):# Check for Nan
            raise ElectronConfigurationError(
                f"\n::No atomic number found for element {element}:: -> CHEM.get_atomic_number()")

        return atomic_number

    # Takes the number of elementary elements (atoms or compounds), returns the mass of in grams
    def atoms_to_mass(self, quantity: int, chemical: str) -> float:
        """
        chem = Chem()
        chem.atoms_to_mass(2.35e24, "Cu1") # returns ~ 248
        """

        molar_mass = self.get_compound_molarmass(chemical)

        return (quantity * molar_mass) / self.AVOGADRO

    # Calculates molar_mass of element
    def get_element_molarmass(self, element: str) -> float:
        """
        chem = Chem()
        chem.get_element_molarmass('He') # returns ~ 4.0
        """

        if element not in self.elements_df["element"].values:
            raise ValueError("\n::NO SUCH ELEMENT:: -> CHEM.get_element_molar_mass")

        return self.elements_df.loc[self.elements_df["element"] == element]["molar_mass"].values[0]

    # Calculates the number of elementary elements in a compound
    def get_elementary_elements(self, compound: str, element_g: Union[int, float]) -> float:
        """
        chem = Chem()
        chem.get_elementary_elements('c', 12.0) # returns 6.022e23
        """

        molar_mass = self.get_compound_molarmass(compound)
        return (element_g * self.AVOGADRO) / molar_mass

    # Returns molar_mass of compound
    def get_compound_molarmass(self, compound: str) -> float:
        """
        chem = Chem()
        chem.get_compound_molarmass("H2O1") # returns ~ 18.0
        """

        return self.__calculate_compound_molarmass(compound, 0, 0.0)


    # Get group of element symbol
    def get_group(self, element: str) -> str:
        """
        chem = Chem()
        chem.get_group('H') # returns Nonmetal
        """

        if element not in self.elements_df["element"].values:
            raise ValueError("\n::NO SUCH ELEMENT:: -> CHEM.get_group")

        group_block = self.elements_df.loc[self.elements_df["element"] == element]["GroupBlock"].values[0]
        
        if pd.isna(group_block):  # Check for Nan
            raise groupBlockError(
                f"\n::No block found for element {el}:: -> CHEM.get_group()")
            
        return group_block

    # Gets Electron configuration of an element
    def get_electron_configuration(self, el: str) -> str:
        """
        chem = Chem()
        chem.get_electron_configuration("He") # returns "1s2"
        """

        if el not in self.elements_df["element"].values:
            raise ValueError("\n::NO SUCH ELEMENT:: -> CHEM.get_electron_configuration()")

        electron_configuration = self.elements_df.loc[self.elements_df["element"] == el]["ElectronConfiguration"].values[0]

        if pd.isna(electron_configuration):  # Check for Nan
            raise ElectronConfigurationError(
                f"\n::No electron configuration found for element {el}:: -> CHEM.get_electron_configuration()")

        return electron_configuration

    def WALTERWHITE(self) -> str:
        print(
            " ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣿⣿⠿⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⡏⠁⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣶⣶⣶⣶⣦⣤⡄⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣷⣄⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡧⠇⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣿⣿⣿⣿⣾⣮⣭⣿⡻⣽⣒⠀⣤⣜⣭⠐⢐⣒⠢⢰⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⡟⣾⣿⠂⢈⢿⣷⣞⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣷⣶⣾⡿⠿⣿⠗⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⠋⠉⠑⠀⠀⢘⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣿⣿⣿⣿⣿⡿⠟⢹⣿⣿⡇⢀⣶⣶⠴⠶⠀⠀⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣿⣿⣿⣿⡿⠀⠀⢸⣿⣿⠀⠀⠣⠀⠀⠀⠀⠀⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠹⣿⣧⣀⠀⠀⠀⠀⡀⣴⠁⢘⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿\n" +
            " ⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⠗⠂⠄⠀⣴⡟⠀⠀⡃⠀⠉⠉⠟⡿⣿⣿⣿⣿\n" +
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⠾⠛⠂⢹⠀⠀⠀⢡⠀⠀⠀⠀⠀⠙⠛⠿⢿\n\n" +
            "Say My Name ");
