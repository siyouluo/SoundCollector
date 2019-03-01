/**
  ***************************************************************
  * @file    IndicatorLight.c
  * @author  Siyou luo
  * @contact siyouluo11@gmail.com
  * @version V1.0
  * @date    27-JAN-2019
  * @brief   指示灯驱动程序，用来提示系统运行以及bug调试
  ******************************************************************************
  * @resources
  * GPIOC_Pin_13
  * 系统板上的黄绿色led灯
  ******************************************************************************
  */
#include "IndicatorLight.h"
void LED_Init()
{
	GPIO_InitTypeDef GPIO_InitStructure;//定义结构体变量
	
	RCC_APB2PeriphClockCmd(LED_PORT_RCC,ENABLE);
	
	GPIO_InitStructure.GPIO_Pin=LED_PIN;  //选择你要设置的IO口
	GPIO_InitStructure.GPIO_Mode=GPIO_Mode_Out_PP;	 //设置推挽输出模式
	GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;	  //设置传输速率
	GPIO_Init(LED_PORT,&GPIO_InitStructure); 	   /* 初始化GPIO */
	
	GPIO_SetBits(LED_PORT,LED_PIN);   //将LED端口拉高，熄灭所有LED
}

