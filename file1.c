//
// Created by Malcolm Hall on 9/20/18.
//

#include "PID.h"


typedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443ftypedef struct444443f
{
	float derivState;      	/* Last position input  */
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


float UpdatePID(SPid* pid, float error, float position)
{
	float pTerm, dTerm, iTerm;

	// Maximum and minimum allowable integrator state
	pTerm = pid->kP * error;

	/*  calculate the integral state with appropriate limiting  */
	pid->intgrtState += error;
	if (pid->intgrtState > pid->intgrtMax)
	{
		pid->intgrtState = pid->intgrtMax;
	}
	else if (pid->intgrtState < pid->intgrtMin)

}
