#include "buzz_controller_drone_sim.h"
#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <stdio.h>
#include <sstream>
#include <algorithm>
#include <cmath>
#include <json/json.h>

namespace buzz_drone_sim {

const std::string RESULT_FILE = "results/result.txt";
const std::string RADIATION_SOURCES_FILE = "data/radiation_sources.json";

/****************************************/
/****************************************/

CBuzzControllerDroneSim::CBuzzControllerDroneSim() : CBuzzControllerSpiri() {
   std::chrono::high_resolution_clock::time_point previous = 
      std::chrono::high_resolution_clock::now();
   usleep(10);
   std::chrono::high_resolution_clock::duration duration(
      std::chrono::high_resolution_clock::now() -  previous);
   random_engine_.seed(duration.count());

   remove(RESULT_FILE.c_str());
}

/****************************************/
/****************************************/

CBuzzControllerDroneSim::~CBuzzControllerDroneSim() {
}

/****************************************/
/****************************************/

void CBuzzControllerDroneSim::Init(TConfigurationNode& t_node)  {
   CBuzzControllerSpiri::Init(t_node);
   m_pcCamera->Enable();
}

/****************************************/
/****************************************/

void CBuzzControllerDroneSim::GoTo(const CVector2& position) {
   CVector3 new_position;

   new_position.SetX(position.GetX());
   new_position.SetY(position.GetY());
   new_position.SetZ(5.0f); // To ensure that the quadrotor flies
   
   m_pcPropellers->SetAbsolutePosition(new_position);
}

/****************************************/
/****************************************/

bool CBuzzControllerDroneSim::HasReached(const CVector2& position, const float& delta) {
   float difference = std::sqrt(
      std::pow(m_pcPos->GetReading().Position.GetX() - position.GetX(),2)+
      std::pow(m_pcPos->GetReading().Position.GetY() - position.GetY(),2));

   return difference < delta;   
}

/****************************************/
/****************************************/

std::string CBuzzControllerDroneSim::GetCurrentKey(){
   int x = static_cast<int>(std::rint(m_pcPos->GetReading().Position.GetX()));
   int y = static_cast<int>(std::rint(m_pcPos->GetReading().Position.GetY()));
   std::string key = std::to_string(x) + '_' + std::to_string(y);
   return key;
}

/****************************************/
/****************************************/

float CBuzzControllerDroneSim::GetCurrentElevation(){
   //return m_pcPos->GetReading().Position.GetZ();
   std::normal_distribution<float> noise_distribution(0.0, 0.1);
   float noise = noise_distribution(random_engine_);
   return std::sin(m_pcPos->GetReading().Position.GetX()) + noise;
}

/****************************************/
/****************************************/

float CBuzzControllerDroneSim::GetRadiationIntensity(){
   Json::Value radiationValues;
   Json::Reader reader;
   std::ifstream radiationFile(RADIATION_SOURCES_FILE);

   reader.parse(radiationFile, radiationValues);

   int x = static_cast<int>(std::rint(m_pcPos->GetReading().Position.GetX()));
   int y = static_cast<int>(std::rint(m_pcPos->GetReading().Position.GetY()));
   
   float totalRadiationIntensity = 0.0;
   for (auto source : radiationValues){
      RadiationSource radiation = RadiationSource(source["x"].asFloat(), source["y"].asFloat(), source["intensity"].asFloat());
      totalRadiationIntensity += radiation.GetPerceivedIntensity(x, y);
   }
   // Normal distribution (mean, std)
   std::normal_distribution<float> noise_distribution(0.0, 0.05);
   float noise = noise_distribution(random_engine_);

   // Compute belief elem [0,1]
   float radiation_belief = totalRadiationIntensity + noise;
   if (radiation_belief < 0.0) {
      radiation_belief = 0.0;
   } else if (radiation_belief > 1.0) {
      radiation_belief = 1.0;
   }

   return radiation_belief;
}

/****************************************/
/****************************************/

void CBuzzControllerDroneSim::LogDatum(const std::string& key, const float& data, const int& step){
   std::string parsed_key = key;
   std::replace(parsed_key.begin(), parsed_key.end(), '_', ' ');
   std::stringstream ss(parsed_key);
   int x, y;
   ss >> x >> y;

   std::ofstream result_file;
   result_file.open(RESULT_FILE, std::ios::out | std::ios::app);

   float weight = 1.0;
   result_file << x << " " << y << " " << data << " " << weight << " " << step << std::endl;
}

}