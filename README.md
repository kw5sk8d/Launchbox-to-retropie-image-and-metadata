# Launchbox-to-retropie-image-and-metadata
//WHAT I WANT TO DO...
//done	//-Check what "rom_list" I have on a particular retropie either by a "gamelist.xml" crawl or a folder crawl.
//done	//-Take that "rom_list" copy and organize requested game images into a "file_structure" the retropie/es can use 
//done	//-Creates and poputaltes a "file_structure" that can be copied the retropie, *hint: you should maybe create a backup? 
//done	//-Resize imported images so the little pie that could doesn't freakout
//done	//-Update the "gamelist.xml" with the details from "rom_list" with paths and filesname of specific items by <game> files

#BLUF: Open and modify the user inputs based on the notes and it shits out a file structure that can be read by retropie/ES everything is local to the script. Thinking of adding this to my GIT? never know.

WHAT IT ACTUALLY DOES: So far... everything I want it to.

//
//HOMEWORK
//
	//looks like there are images and files that are able parse from launchbox to retropie with a script to the gamelist.xml
	//there is a script that looks like it might do thins for me but will probably need some tweaking...@
		//https://forums.launchbox-app.com/files/file/860-launchbox-retropie-batocera-miyoo-export/?tab=comments
	//UPDATE// That script was a bust! it tried but was a little too weird for the limited knowledge of python code.  

//@ https://github.com/RetroPie/EmulationStation/blob/master/GAMELISTS.md

// checked on 27may25

//@EmulationStation/es-app/src/MetaData.cpp

//MetaDataDecl gameDecls[] = { //pretty sure this is for the game entries
//	// key,         type,                   default,            statistic,  name in GuiMetaDataEd,  prompt in GuiMetaDataEd
//	{"name",        MD_STRING,              "",                 false,      "name",                 "enter game name"},
//	{"sortname",    MD_STRING,              "",                 false,      "sortname",             "enter game sort name"},
//	{"image",       MD_PATH,                "",                 false,      "image",                "enter path to image"},
//	{"video",       MD_PATH     ,           "",                 false,      "video",                "enter path to video"},
//	{"marquee",     MD_PATH,                "",                 false,      "marquee",              "enter path to marquee"},
//	{"thumbnail",   MD_PATH,                "",                 false,      "thumbnail",            "enter path to thumbnail"},
//};

//MetaDataDecl folderDecls[] = { // for the folders i guess
//	{"name",        MD_STRING,              "",                 false,      "name",                 "enter game name"},
//	{"sortname",    MD_STRING,              "",                 false,      "sortname",             "enter game sort name"},
//	{"desc",        MD_MULTILINE_STRING,    "",                 false,      "description",          "enter description"},
//	{"image",       MD_PATH,                "",                 false,      "image",                "enter path to image"},
//	{"thumbnail",   MD_PATH,                "",                 false,      "thumbnail",            "enter path to thumbnail"},
//	{"video",       MD_PATH,                "",                 false,      "video",                "enter path to video"},
//	{"marquee",     MD_PATH,                "",                 false,      "marquee",              "enter path to marquee"},
//};

//data i want parsed from launchbox metadata --> update retropie/es gameslist.xml

//<game>
	"name", //as scraped i trust launch box over es
	"sortname", //as scraped i trust launch box over es
	"image", //boxes
	"video", //in progress
	"marquee", //marquee or logos
	"thumbnail", //clear logo maybe screenshots 
//</game> 

//
//Things i need to figure out 
//

//what i dont know is if I can append the gamelist.xml or do I need to create a new one?
//what happens when a new rom is added
//test what each item looks like on the es themed frontends on the retropie so im not completely wasting my time.

//
//Things I know
//

//The switch --gamelist-only can be used to skip automatic searching, and only display games defined in the system's gamelist.xml.
//The switch --ignore-gamelist can be used to ignore the gamelist and force ES to use the non-detailed view.

//
//END HOMEWORK
//

//Alright I got it working with the help of Bitchin Bette! We started from scratch. I might go into more detail here but ill include an BLUF.
//Here is the result
