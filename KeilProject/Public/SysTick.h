#ifndef _SYSTICK_H
#define _SYSTICK_H

#include "system.h"

void SysTick_Init(u8 SYSCLK);
void delay_ms(u16 nms);
void delay_us(u32 nus);


#endif
