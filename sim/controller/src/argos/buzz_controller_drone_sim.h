#ifndef BUZZ_CONTROLLER_DRONE_SIM_H
#define BUZZ_CONTROLLER_DRONE_SIM_H

#include <buzz/argos/buzz_controller_spiri.h>
#include <argos3/plugins/robots/generic/control_interface/ci_quadrotor_position_actuator.h>
#include <argos3/plugins/robots/generic/control_interface/ci_colored_blob_perspective_camera_sensor.h>

#include <random>
#include <chrono>
#include <vector>

#include "radiation_source.h"

using namespace argos;

namespace buzz_drone_sim {

/*
* Buzz controller
*/
class CBuzzControllerDroneSim : public CBuzzControllerSpiri {

public:

   CBuzzControllerDroneSim();
   
   virtual ~CBuzzControllerDroneSim();

   virtual void Init(TConfigurationNode& t_node);

   // Control functions
   void GoTo(const CVector2& position);

   std::default_random_engine& GetRandomEngine()
   {
      return random_engine_;
   }

   bool HasReached(const CVector2& position, const float& delta);

   std::string GetCurrentKey();

   float GetCurrentElevation();

   float GetRadiationIntensity();

   void LogDatum(const std::string& key, const float& data, const int& step);
   
   void LogDataSize(const int& total_data, const int& step);

protected:

   virtual buzzvm_state RegisterFunctions();

private:

   std::default_random_engine random_engine_;

};
}
#endif
