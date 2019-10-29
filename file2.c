// Created by Malcolm Hall on 9/20/18.
//asdf

#include "PID.h"




typedef struct44asdf4443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443f
{
	float derivState;      	/* Last position input
	*/
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
//other comment

}
void InitPID(Spid* pid, float kP, float kI, float kD, float iMin, float iMax)
{
	pid->kP = kP;
	pid->kI = kI;
	pid->k_D = kD;
	pid->intgrtMin = iMin;
	pid->intgrtMax = iMax;
}
//other comment

}
void InitPID(Spid* pid, float kP, float kI, float kD, float iMin, float iMax)
{
	pid->kP = kP;
	pid->kI = kI;
	pid->k_D = kD;
	pid->intgrtMin = iMin;
	pid->intgrtMax = iMax;
}
//other comment

}