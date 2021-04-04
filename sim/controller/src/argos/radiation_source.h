#include <math.h>

namespace buzz_drone_sim {

class RadiationSource
{
    private:
        const float x;
        const float y;
        const float intensity;
        
    public:
        RadiationSource(const float x, const float y, const float intensity);
        float GetIntensity();
        float GetPerceivedIntensity(const int x, const int y);
};

}
