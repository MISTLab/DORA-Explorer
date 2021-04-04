#include "radiation_source.h"


namespace buzz_drone_sim {

/****************************************/
/****************************************/

RadiationSource::RadiationSource(const float x, const float y, const float intensity)
    : x(x), y(y), intensity(intensity) {}

/****************************************/
/****************************************/

float RadiationSource::GetIntensity() {
    return this->intensity;
}

}
