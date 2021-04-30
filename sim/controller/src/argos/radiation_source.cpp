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

float RadiationSource::GetPerceivedIntensity(const int x, const int y) {
    float distance = sqrt(pow(this->x - x, 2.0) + pow(this->y - y, 2.0));

    return this->intensity / (1 + 0.20*pow(distance, 2.0));
}

CVector3 RadiationSource::GetCoordinates() {
    return CVector3(this->x, this->y, 0.0);
}

}
