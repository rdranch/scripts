# pip3 install -r requirements.txt
# Created by Russell Dranch
# github.com/rdranch/scripts
#
#
import os
from sys import argv
from re import finditer, IGNORECASE, escape
from magic import Magic
from tqdm import tqdm

# TODO: Add iOS support

custom = {
    "Multi Scan":"(private|dev|secret|developer|session|API|access|user)[-|_|\s|:|.](key|token|password|user|id).{20}",
    "Singular Scan":"(password|username|user|userId|token|accessKey|sessionId|APIKey|oauth|webcredential|private)(?=.*?:)(\S{20})(.|\s)(\S{10})"
}

#Github: https://github.com/l4yton/RegHex
regular = {
    "Artofactory API Token":"(?:\s|=|:|\"|^)AKC[a-zA-Z0-9]{10,}",
    "Artifactory Password":"(?:\s|=|:|\"|^)AP[\dABCDEF][a-zA-Z0-9]{8,}",
    "Authorization basic":"basic [a-zA-Z0-9_\\-:\\.=]+",
    "Authroization Bearer":"bearer [a-zA-Z0-9_\\-\\.=]+",
    "AWS Client ID":"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
    "AWS MWS Key":"amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    "AWS Secret Key1":"(?i)aws(.{0,20})?(?-i)['\"][0-9a-zA-Z\/+]{40}['\"]",
    "Base64":"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})$",
    "Basic Auth Credentials":"(?<=:\/\/)[a-zA-Z0-9]+:[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+",
    "Cloudinary Basic Auth":"cloudinary:\/\/[0-9]{15}:[0-9A-Za-z]+@[a-z]+",
    "Facebook Access Token":"EAACEdEose0cBA[0-9A-Za-z]+",
    "Facebook Client ID":"(?i)(facebook|fb)(.{0,20})?['\"][0-9]{13,17}",
    "Facebook Oauth":"[f|F][a|A][c|C][e|E][b|B][o|O][o|O][k|K].*['|\"][0-9a-f]{32}['|\"]", # potential issue
    "Facebook Secret Key":"(?i)(facebook|fb)(.{0,20})?(?-i)['\"][0-9a-f]{32}",
    "Github":"(?i)github(.{0,20})?(?-i)['\"][0-9a-zA-Z]{35,40}",
    "Google API Key":"AIza[0-9A-Za-z\\-_]{35}",
    "Google Cloud Platform API Key":"(?i)(google|gcp|youtube|drive|yt)(.{0,20})?['\"][AIza[0-9a-z\\-_]{35}]['\"]",
    "Google Drive API Key":"AIza[0-9A-Za-z\\-_]{35}",
    "Google Drive Oauth":"[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com",
    "Google Gmail API Key":"AIza[0-9A-Za-z\\-_]{35}",
    "Google Gmail Oauth":"[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com",
    "Google Oauth Access Token":"ya29\\.[0-9A-Za-z\\-_]+",
    "Google Youtube API Key":"AIza[0-9A-Za-z\\-_]{35}",
    "Google Youtube Oauth":"[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\\.com",
    "Heroku API Key":"[h|H][e|E][r|R][o|O][k|K][u|U].{0,30}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}",
    "IPv4":"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}\b",
    "Javascript Variables":"(?:const|let|var)\s+\K(\w+?)(?=[;.=\s])",
    "LinkedIn Client ID":"(?i)linkedin(.{0,20})?(?-i)['\"][0-9a-z]{12}['\"]",
    "LinkedIn Secret Key":"(?i)linkedin(.{0,20})?['\"][0-9a-z]{16}['\"]",
    "Mailchamp API Key":"[0-9a-f]{32}-us[0-9]{1,2}",
    "Mailgun API Key":"key-[0-9a-zA-Z]{32}",
    "Mailto:":"(?<=mailto:)[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+",
    "Picatic API Key":"sk_live_[0-9a-z]{32}",
    "Slack Token":"xox[baprs]-([0-9a-zA-Z]{10,48})?",
    "Slack Webhook":"https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
    "Stripe API Key":"(?:r|s)k_live_[0-9a-zA-Z]{24}",
    "Square Access Token":"sqOatp-[0-9A-Za-z\\-_]{22}",
    "Square Oauth Secret":"sq0csp-[ 0-9A-Za-z\\-_]{43}",
    "Twilio API Key":"SK[0-9a-fA-F]{32}",
    "Twitter Client ID":"(?i)twitter(.{0,20})?['\"][0-9a-z]{18,25}",
    "Twitter Oauth":"[t|T][w|W][i|I][t|T][t|T][e|E][r|R].{0,30}['\"\\s][0-9a-zA-Z]{35,44}['\"\\s]",
    "Twitter Secret Key":"(?i)twitter(.{0,20})?['\"][0-9a-z]{35,44}",
    "Vault Token":"[sb]\.[a-zA-Z0-9]{24}",
    "URLs With HTTP Protocol":"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
}

def _map_files(apk, map=dict()):
    '''Creates an empty mapping of all files which are not in the 'blockers' list

    Arguments
    ---------
    apk : String
        The location path of the apk to scan
    map : dictionary
        A dictionary in which to create the mapping

    Returns
    -------
    map : dictionary
    '''
    blockers = {'image/gif', 'audio/mpeg', "image/jpg", "image/png", "font/sfnt", "video/mp4", "application/font-sfnt", "application/vnd.ms-opentype"}

    for subdir, dirs, files in os.walk(apk):
        for f in files:
            if subdir == "original":
                continue
            file_type = Magic(mime=True).from_file(os.path.join(subdir, f))
            if file_type in blockers or f == "CodeResources":
                continue

            map[os.path.join(subdir, f)] = list()

    return map

def output(mapping, file_name="creds.txt"):
    '''Outputs non-empty mappings found

    Arguments
    ---------
    mapping : dictionary
        Taken from _map_files() of all files/patterns
    file_name : string
        Name of file to create
    '''
    with open(file_name, "a+") as f:
        for key, value in mapping.items():
            if value == []:
                continue
            f.write("\n"+"="*100+"\n"+key+"\n"+"="*100+"\n")
            for v in value:
                f.write(str(v)+"\n")

    print(f"> {file_name} created in {os.getcwd()}\n> Size of {file_name}: {os.path.getsize(file_name)} bytes")

def search(apk, regList):
    '''Searches for credentials regex patterns line-by-line in APK files

    Arguments
    ---------
    apk : String
        The location path of the apk to scan
    regList : Dictionary
        Dictionary list of regex pattern to use

    Returns
    -------
    mapping : dictionary
    '''
    print("> Beginning credential search")
    mapping = _map_files(apk)
    print("> Finishing mapping files")

    for key, value in tqdm(mapping.items()):
        for regex in regList:
            for i, line in enumerate(open(key, encoding="utf8", errors='ignore')):
                try:
                    for match in finditer(regList[regex], escape(line), flags=IGNORECASE):
                        value.append(f"{regex}:\t{match.group()}\t:{i+1}")
                except:
                    continue
    return mapping

def get_answer():
    '''Gets user answer for which regex pattern to use

    Returns
    -------
    custom : dictionary
    regular: dictionary
    '''
    check = input("> Use regular regex or custom regex? (c/r): ")

    while check not in ["c", "custom", "r", "regular"]:
        check = input("> Use regular regex or custom regex? (c/r): ")

    if check == "c" or check == "custom":
        return custom
    return regular


if __name__ == "__main__":
    try:
        file = argv[1]
        if os.path.isdir(file):
            output(search(file, get_answer()))
            print("> Done.")
        else:
            print("> The file given is not a dir")
    except KeyboardInterrupt:
        print("\n> Quitting.")
    except IndexError:
        print("> Script needs a dir to scan.")

    