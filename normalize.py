import re
import regex


def __call__(self, s: str):
    # s = s.lower()
    # s = re.sub(r"[<\[][^>\]]*[>\]]", "", s)  # remove words between brackets
    # s = re.sub(r"\(([^)]+?)\)", "", s)  # remove words between parenthesis
    s = self.clean(s).lower()

    if self.split_letters:
        s = " ".join(regex.findall(r"\X", s, regex.U))

    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\n+", " ", s)
    s = re.sub(r"\r+", " ", s)
    # replace any output that can screw up the terminal display
    s = re.sub(r"\u001B\[(?:[0-9]{1,3}[ABCDEFGHJKSTfm]|8m|2K|H)", "", s)
    return s.strip()
