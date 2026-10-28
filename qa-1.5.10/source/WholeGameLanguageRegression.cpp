#define main previousBaselineMain
#include "ThirdUpgradeBaseline.cpp"
#undef main
#include "../../lib/mapping/CMapService.h"
#include "../../lib/mapping/CMap.h"
#include "../../lib/callback/EditorCallback.h"
#include "../../lib/texts/CGeneralTextHandler.h"
#include "../../lib/mapObjects/CQuest.h"
#include "../../lib/campaign/CampaignHandler.h"
int main(){try{
 LIBRARY=new GameLibrary;LIBRARY->initializeFilesystem(false);LIBRARY->initializeLibrary();
 const auto language=LIBRARY->generaltexth->getPreferredLanguage();
 const auto expectedLanguage=language=="czech"?std::string("english"):language;
 const JsonNode expected(JsonPath::builtin("translation/dragon-citadel/"+expectedLanguage+".json"));
 JsonNode report;int strings=0;
 for(const auto &[key,value]:expected.Struct()){
  const auto actual=LIBRARY->generaltexth->translate(key);
  if(actual!=value.String())throw std::runtime_error("Translation mismatch: "+key+" actual="+actual+" expected="+value.String());
  ++strings;
 }

 if(language!="czech"){
  const JsonNode baseExpected(JsonPath::builtin(language=="english"?"config/h3forvcmienglisation/game.json":"config/vcmi-"+language+"/game.json"));
  const JsonNode engineExpected(JsonPath::builtin("config/"+language+".json"));
  int compared=0; int engineOverrides=0;
  for(const auto &[key,value]:baseExpected.Struct()){
   const auto actual=LIBRARY->generaltexth->translate(key);
   if(actual!=value.String()){
    if(engineExpected[key].isString() && actual==engineExpected[key].String())++engineOverrides;
    else throw std::runtime_error("Base game translation mismatch: "+key+" actual="+actual+" expected="+value.String());
   }
   ++compared;
  }
  require(compared>6000,"Base game translation missing");
  report["baseGameStringsCompared"].Integer()=compared;
  report["verifiedEngineOverrides"].Integer()=engineOverrides;
 }

 if(std::getenv("DC_EXPORT_WOG_TEXTS")){
  const JsonNode keys(JsonPath::builtin("translation/wog-polish-source.json"));JsonNode actual;
  for(const auto &[key,value]:keys.Struct())actual[key].String()=LIBRARY->generaltexth->translate(key);
  std::ofstream("wog-actual-"+language+".json")<<actual.toString();
 }
 if(std::getenv("DC_VERIFY_WOG_TEXTS")){
  const JsonNode extra(JsonPath::builtin("translation/wog-eight-languages/"+language+".json"));
  for(const auto &[key,value]:extra.Struct())require(LIBRARY->generaltexth->translate(key)==value.String(),("WoG translation mismatch: "+key).c_str());
  report["optionalWoGStringsCompared"].Integer()=extra.Struct().size();
 }
 CMapService service;EditorCallback cb(nullptr);
 for(int chapter=1;chapter<=8;++chapter){
  const auto n=std::string("0")+std::to_string(chapter);
  auto map=service.loadMap(ResourcePath("MAPS/DC_"+n,EResType::MAP),&cb);cb.setMap(map.get());
  require(map->name.toString()==expected["dragon-citadel.map"+n+".dc.header.name"].String(),"Map title translation mismatch");
  int quests=0;
  for(const auto & object:map->objects)if(auto * hut=dynamic_cast<const CGSeerHut *>(object.get())){
   const auto text=hut->getQuest().firstVisitText.toString();
   require(!text.empty() && text.find("map.")!=0 && text.find("dc.")!=0,"Unresolved quest text ID");
   ++quests;
  }
  require(quests==1,"Missing translated optional quest");
  report["chapters"][n]["title"].String()=map->name.toString();report["chapters"][n]["questResolved"].Bool()=true;
  std::cout<<"PASS translated map "<<language<<" chapter="<<chapter<<std::endl;
  cb.setMap(nullptr);
 }
 auto campaign=CampaignHandler::getCampaign("MAPS/SMOCZA_CYTADELA");require(campaign->scenariosCount()==8,"Campaign lost chapters");
 require(campaign->getDescriptionTranslated().find(expected["dragon-citadel.status.visualWork"].String())!=std::string::npos,"Campaign description missing translated work-in-progress notice");
 for(const auto & id:campaign->allScenarios()){
  const auto & scenario=campaign->scenario(id);
  require(!scenario.regionText.toString().empty(),"Empty translated campaign region");
  const auto chapter=std::string("0")+std::to_string(id.getNum()+1);
  require(scenario.regionText.toString()==expected["dragon-citadel.campaign.chapter"+chapter+".regionText"].String(),"Campaign region translation mismatch");
  auto embedded=campaign->getMap(id,&cb);require(!embedded->name.toString().empty(),"Embedded translated map failed");
 }
 report["language"].String()=language;report["stringsCompared"].Integer()=strings;report["campaignEmbeddedMapsLoaded"].Integer()=8;report["success"].Bool()=true;
 std::ofstream("eight-language-native-"+language+".json")<<report.toString();std::cout<<"PASS "<<language<<" native keys="<<strings<<" maps=8 embedded=8"<<std::endl;return 0;
}catch(const std::exception & e){std::cerr<<"FAIL "<<e.what()<<std::endl;return 1;}}

