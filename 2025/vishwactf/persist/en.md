# Persist
# Forensic
# Description:
> User, “I logged onto my computer on FRIDAY and noticed something on the home screen before the computer shut down. Could it have been malware?”

# Given
- HKLM/SOFTWARE
- HKCU

# Solution

As usual what are those file?

```bash
file HKLM/SOFTWARE 
HKLM/SOFTWARE: MS Windows registry file, NT/2000 or above
file HKCU 
HKCU: MS Windows registry file, NT/2000 or above
```

So they are windows registry file. Those are binary except extracting the strings or viewing them with the proper tool we can't do much with them.

I found out regripper `https://github.com/keydet89/RegRipper3.0`

```
Regripper’s CLI tool can be used to surgically extract, translate, and display information (both data and metadata) from Registry-formatted files via plugins in the form of Perl-scripts. It allows the analyst to select a hive-file to parse and a plugin or a profile, which is a list of plugins to run against the given hive. The results go to STDOUT and can be redirected to a file, that the analyst designates.
```

Sounds like what I need!

```bash
regripper -r HKLM/SOFTWARE -a > software.txt
regripper -r HKCU -a > hkcu.txt
```

Then I proceed to analyse those file manually and it did not took long before finding this interesting snippet

```
RecentDocs
**All values printed in MRUList\MRUListEx order.
Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs
LastWrite Time: 2025-02-27 17:35:52Z
  5 = Silent Files
  8 = p0wer}.txt
  7 = _r3g.txt
  6 = _in.txt
  4 = {b3l1ef.txt
  3 = 
  2 = RegistryExplorer.zip
  1 = 
  0 = 
```
So I tried to submit the following:

`VishwaCTF{b3l1ef_in_r3g_p0wer}`

And rawr does the dinosaur