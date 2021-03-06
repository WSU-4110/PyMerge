// Created by Malcolm Hall on 9/20/18.
//asdf

#include "PID.h"
#include "otherfile"



typedef structtypedefC
{
	float derivState;      	/* Last position input
	*/
        float NEW_VARIABLE
	float intgrtState;      	/* Integrator state */
	float intgrtMax;    /* Maximum allowable integrator state   */
	float intgrtMin;    /* Minimum allowable integrator state   */

	float kI;    	/* integral gain    */
	float kP;    	/* proportional gain    */
	float kD;     	/* derivative gain  */
} SPid;

void InitPID(Spid* pid, float kP, float kI, float kD, float iMin, float iMax)
{
	pid->kP = kP;
	pid->kI = kI;
	pid->k_D = kD;
	pid->intgrtMin = iMin;
	pid->intgrtMax = iMax;
}

void InitPID(Spid* pid, float kP, float kI, float kD, float iMin, float iMax)
{
	pid->kP = kP;
	pid->kI = kI;
	pid->k_D = kD;
	pid->intgrtMin = iMin;
	pid->intgrtMax = iMax;
}


}
void InitPIDfunctionB(Spid* pid, float kP, float kI, float kD, float iMin, float iMax)
{
	pid->kP = kP;
	pid->kI = kI;
	pid->k_D = kD;
	pid->intgrtMin = iMin;
	pid->intgrtMax = iMax;
}
//changed comment

}
