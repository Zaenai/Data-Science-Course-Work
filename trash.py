import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import wordnet
from nltk.corpus import stopwords
#nltk.download('all')
str = "donald trump has the unnerving ability to ability to create his own reality and convince millions of americans that what he says it is true the problem with the president lying is that he then believes his own lies a new poll shows how that can get the country into deep trouble the new abc news washington post poll came out after the president s physician gave him a physical and mental exam the doctor gave trump a clean bill of health added an inch to his height and claimed he was fit to serve for seven more years this poll was able to capture americans opinions after a new book came out indicating that people around trump questioned his emotional stability and ability to hold office in addition the new poll gave the respondents the time to hear trump tell the public that he was a very stable genius before they were interviewed he said actually throughout my life my" 
str2 = "two greatest assets have been mental stability and being like really smart the abc washington post poll discovered that <number> percent of the people it interviewed believed that the president was a genius that left a full <number> percent who saw through that lie then there was the question of trump s mental stability the poll found that there was a nearly even divide throughout the nation when asked if the president was stable <number> percent of those interviewed said he was not but <number> percent believed he is stable the abc news washington post poll was taken from <date> through <number> <number> the random sample consisted of <number> adults interviewed by landline and cell phone in both english and spanish the margin of error was  <number> <number> percentage points featured image via getty images drew angerer"

lemmatizer = WordNetLemmatizer()


# switch tags, compatibility with lemmatise() 
def switchTag(tag):
    if tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('V'):
        return wordnet.VERB
    elif (tag.startswith('J') or
            tag.startswith('A')):
        return wordnet.ADJ
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        print(tag)
        return wordnet.NOUN #''

# lemmatise with respect to tag
def lemmatisation(str,lemmatizer,type):
    str_token = word_tokenize(str)
    retVal = []
    for word in str_token:
        retVal.append(lemmatizer.lemmatize(word,pos=type))
    return retVal


# # Use it to count dates/numbers 
# tx = "<date> and not date <date>"
# tx = tx.replace('<date>','')
# difference between old and new tx is number of dates

tx = "clintonobama emails key to understanding why hillary wasn t indicted andrew mccarthy headline bitcoin blockchain searches exceed trump blockchain stocks are next by andrew c mccarthy family security matters new fbi texts highlight a motive to conceal the president s involvement from the first these columns have argued that the whitewash of the hillary clinton emails caper was president barack obama s call not the fbi s and not the justice department s see e g here here and here the decision was inevitable obama using a pseudonymous email account had repeatedly communicated with secretary clinton over her private non secure email account these emails must have involved some classified information given the nature of consultations between presidents and secretaries of state the broad outlines of obama s own executive order defining classified intelligence see eo <number> section <number> <number> and the fact that the obama administration adamantly refused to disclose the clinton obama emails if classified information was mishandled it was necessarily mishandled on both ends of these email exchanges if clinton had been charged obama s culpable involvement would have been patent in any prosecution of clinton the clinton obama emails would have been in the spotlight for the prosecution they would be more proof of willful or if you prefer grossly negligent mishandling of intelligence more significantly for clinton s defense they would show that obama was complicit in clinton s conduct yet faced no criminal charges that is why such an indictment of hillary clinton was never going to happen the latest jaw dropping disclosures of text messages between fbi agent peter strzok and his paramour fbi lawyer lisa page illustrate this point for the moment i want to put aside the latest controversy the fbi s failure to retain five months of text messages between strzok and page those chattiest of star crossed lovers yes this glitch closes our window on a critical time in the trump russia investigation mid <date> through mid <date> that is when the bureau and justice department were reportedly conducting and renewing in <number> day intervals court approved fisa surveillance that may well have focused on the newly sworn in president of the united states remember the bureau s then director james comey testified at a <date> house intelligence committee hearing that the investigation was probing possible coordination with trump s campaign and kremlin interference in the election the retention default has been chalked up to a technological mishap assuming that this truly was an indiscriminate bureau wide problem that lost texts are not limited to phones involved in the trump russia investigation it is hard to imagine its going undetected for five months in an agency whose business is information retention but it is not inconceivable attorney general jeff sessions maintains that an aggressive inquiry is underway so let s assume for argument s sake at least that either the texts will be recovered or a satisfactory explanation for their non retention will be forthcoming for now let s stick with the clinton obama emails only <date> comey held the press conference at which he delivered a statement describing mrs clinton s criminal conduct but nevertheless recommending against an indictment we now know that comey s remarks had been in the works for two months and were revised several times by the director and his advisers this past weekend in a letter to the fbi regarding the missing texts senate homeland security committee chairman ron johnson r wis addressed some of these revisions according to senator johnson a draft dated <date> i e five days before comey delivered the final version contained a passage expressly referring to a troublesome email exchange between clinton and obama i note that the fbi s report of its eventual interview of clinton contains a cryptic reference to a <date> email that clinton sent from russia to obama s email address see report page <number> the passage in the <date> draft stated we also assess that secretary clinton s use of a personal email domain was both known by a large number of people and readily apparent she also used her personal email extensively while outside the united states including from the territory of sophisticated adversaries that use included an email exchange with the president while secretary clinton was on the territory of such an adversary emphasis added given that combination of factors we assess it is possible that hostile actors gained access to secretary clinton s personal email account on the same day according to a strzok page text a revised draft of comey s remarks was circulated by his chief of staff jim rybicki it replaced the president with another senior government official this effort to obscure obama s involvement had an obvious flaw it would practically have begged congressional investigators and enterprising journalists to press for the identification of the senior government official with whom clinton had exchanged emails that was not going to work consequently by the time comey delivered his remarks on <date> the decision had been made to avoid even a veiled allusion to obama instead all the stress was placed on clinton who was not going to be charged anyway for irresponsibly sending and receiving sensitive emails that were likely to have been penetrated by hostile intelligence services comey made no reference to clinton s correspondent we also assess that secretary clinton s use of a personal e mail domain was both known by a large number of people and readily apparent she also used her personal e mail extensively while outside the united states including sending and receiving work related e mails in the territory of sophisticated adversaries emphasis added given that combination of factors we assess it is possible that hostile actors gained access to secretary clinton s personal e mail account the decision to purge any reference to obama is consistent with the panic that seized his administration from the moment clinton s use of a private non secure server system was revealed in early <date> i detailed this reaction in a series of <number> columns see e g here and here what most alarmed obama and clinton advisers those groups overlap was not only that there were several clinton obama email exchanges but also that obama dissembled about his knowledge of clinton s private email use in a nationally televised interview on <date> just after the new york times broke the news about clinton s email practices at the state department john podesta a top obama adviser and clinton s campaign chairman emailed cheryl mills clinton s confidant and top aide in the obama state department to suggest that clinton s emails to and from potus should be held i e not disclosed because that s the heart of his exec privilege at the time the house committee investigating the benghazi jihadist attack was pressing for production of clinton s emails as his counselors grappled with how to address his own involvement in clinton s misconduct obama deceptively told cbs news in a <date> interview that he had found out about clinton s use of personal email to conduct state department business the same time everybody else learned it through news reports perhaps he was confident that because he had used an alias in communicating with clinton his emails to and from her estimated to number around <number> would remain undiscovered his and clinton s advisers were not so confident right after the interview aired clinton campaign secretary josh scherwin emailed jennifer palmieri and other senior campaign staffers stating jen you probably have more on this but it looks like potus just said he found out hrc was using her personal email when he saw it on the news scherwin s alert was forwarded to mills shortly afterwards an agitated mills emailed podesta we need to clean this up he has emails from her they do not say state gov that is obama had emails from clinton which he had to know were from a private account since her address did not end in state gov as state department emails do so how did obama and his helpers clean this up obama had his email communications with clinton sealed he did this by invoking a dubious presidential records privilege the white house insisted that the matter had nothing to do with the contents of the emails of course rather it was intended to vindicate the principle of confidentiality in presidential communications with close advisers with the media content to play along this had a twofold benefit obama was able <number> to sidestep disclosure without acknowledging that the emails contained classified information and <number> to avoid using the term executive privilege with all its dark watergate connotations even though that was precisely what he was invoking note that claims of executive privilege must yield to demands for disclosure of relevant evidence in criminal prosecutions but of course that s not a problem if there will be no prosecution the white house purported to repair the president s disingenuous statement in the cbs interview by rationalizing that he had meant that he learned of clinton s homebrew server system through news reports he hadn t meant to claim unawareness that she occasionally used private email this was sheer misdirection from obama s standpoint the problem was that he discussed government intelligence matters with the secretary of state through a private email account the fact that in addition clinton s private email account was connected to her own private server system rather than some other private email service was beside the point but again the media was not interested in such distinctions and contentedly accepted the white house s non explanation meanwhile attorney general loretta lynch ordered comey to use the word matter rather than investigation to describe the fbi s probe of clinton s email practices this ensured that the democratic administration s law enforcement agencies were aligning their story with the democratic candidate s campaign rhetoric if there was no investigation there would be no prosecution in <date> in another nationally televised interview obama made clear that he did not want clinton to be indicted his rationale was a legally frivolous straw man clinton had not intended to harm national security this was not an element of the felony offenses she had committed nor was it in dispute no matter obama s analysis was the stated view of the chief executive if as was sure to happen his subordinates in the executive law enforcement agencies conformed their decisions to his stated view there would be no prosecution within a few weeks even though the investigation was ostensibly still underway and over a dozen key witnesses including clinton herself had not yet been interviewed the fbi began drafting comey s remarks that would close the investigation there would be no prosecution on <date> lynch met with clinton s husband former president bill clinton on an out of the way arizona tarmac where their security details arranged for both their planes to be parked over the next few days the fbi took pains to strike any reference to obama s emails with mrs clinton from the statement in which comey would effectively end the matter with no prosecution on <date> amid intense public criticism of her meeting with bill clinton attorney general lynch piously announced that she would accept whatever recommendation the fbi director and career prosecutors made about charging clinton as page told strzok in a text that day this is a purposeful leak following the airplane snafu it was also playacting page elaborated that the attorney general already knows no charges will be brought of course she did it was understood by all involved that there would be no prosecution knowing that lynch had given the fbi notice on <date> that she d be announcing her intention to accept comey s recommendation fearing this just might look a bit choreographed the fbi promptly amended comey s planned remarks to include this assertion which he in fact made on <date> i have not coordinated or reviewed this statement in any way with the department of justice or any other part of the government they do not know what i am about to say but they did not need to participate in drafting the statement and they did not need to know the precise words he was going to use it was not comey s decision anyway all they needed to know was that there would be no prosecution on <date> with the decision that she would not be indicted long since made mrs clinton sat for an interview with the fbi something she d never have done if there were a chance she might be charged the farce was complete with the justice department and fbi permitting two subjects of the investigation mills and clinton aide heather samuelson to sit in on the interview as lawyers representing clinton that is not something law enforcement abides when it is serious about making a case here however it was clear there would be no prosecution all cleaned up no indictment donald trump has the unnerving ability to ability to create his own reality and convince millions of americans that what he says it is true the problem with the president lying is that he then believes his own lies a new poll shows how that can get the country into deep trouble the new abc news washington post poll came out after the president s physician gave him a physical and mental exam the doctor gave trump a clean bill of health added an inch to his height and claimed he was fit to serve for seven more years this poll was able to capture americans opinions after a new book came out indicating that people around trump questioned his emotional stability and ability to hold office in addition the new poll gave the respondents the time to hear trump tell the public that he was a very stable genius before they were interviewed he said actually throughout my life my two greatest assets have been mental stability and being like really smart the abc washington post poll discovered that <number> percent of the people it interviewed believed that the president was a genius that left a full <number> percent who saw through that lie then there was the question of trump s mental stability the poll found that there was a nearly even divide throughout the nation when asked if the president was stable <number> percent of those interviewed said he was not but <number> percent believed he is stable the abc news washington post poll was taken from <date> through <number> <number> the random sample consisted of <number> adults interviewed by landline and cell phone in both english and spanish the margin of error was  <number> <number> percentage points featured image via getty images drew angerer"
tx = tx.replace('<date>','')
tx = tx.replace('<number>','')
tx = word_tokenize(tx)

eng_stopwords = stopwords.words('english')
tx = [word for word in tx if word not in eng_stopwords]


# CD are numbers ; IN can be 'around' or 'like', 'via' etc.
# use it at some point to calculate the real number of <numbers> 
tx = nltk.pos_tag(tx)
        
for index,word in enumerate(tx):
     tx[index] = (word[0],switchTag(word[1]))

for index,word in enumerate(tx):
    tx[index] = lemmatizer.lemmatize(word[0],pos=word[1])


# print(tx)










# print(len(str_lemma))
# print(len(str_lemma2))
# print(len(set(str_lemma)))
# print(len(set(str_lemma2)))

# print(len(set(str_big_lemma)))

# freq = FreqDist(str_big_lemma)
# print(freq.most_common(15))


# from nltk.corpus import wordnet as wn
# from nltk.stem.wordnet import WordNetLemmatizer
# from nltk import word_tokenize, pos_tag
# from collections import defaultdict

# tag_map = defaultdict(lambda : wn.NOUN)
# tag_map['J'] = wn.ADJ
# tag_map['V'] = wn.VERB
# tag_map['R'] = wn.ADV

# text = "Another way of achieving this task"
# tokens = word_tokenize(text)
# lmtzr = WordNetLemmatizer()

# for token, tag in pos_tag(tokens):
#     lemma = lmtzr.lemmatize(token, tag_map[tag[0]])
#     print(token, "=>", lemma)