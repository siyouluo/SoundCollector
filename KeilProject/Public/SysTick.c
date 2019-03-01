#include "SysTick.h"

static u8  fac_us=0;							//us延时倍乘数			   
static u16 fac_ms=0;							//ms延时倍乘数


//初始化延迟函数
//SYSTICK的时钟固定为AHB时钟的1/8
//SYSCLK:系统时钟频率
void SysTick_Init(u8 SYSCLK)
{
	SysTick_CLKSourceConfig(SysTick_CLKSource_HCLK_Div8); 
	fac_us=SYSCLK/8;					
	fac_ms=(u16)fac_us*1000;				   
}								    


/*******************************************************************************
* 函 数 名         : delay_us
* 函数功能		   : us延时，
* 输    入         : nus：要延时的us数
					注意:nus的值,不要大于798915us(最大值即2^24/fac_us@fac_us=21)
* 输    出         : 无
*******************************************************************************/		    								   
void delay_us(u32 nus)
{		
	u32 temp;	    	 
	SysTick->LOAD=nus*fac_us; 					//时间加载	  		 
	SysTick->VAL=0x00;        					//清空计数器
	SysTick->CTRL|=SysTick_CTRL_ENABLE_Msk ;	//开始倒数	  
	do
	{
		temp=SysTick->CTRL;
	}while((temp&0x01)&&!(temp&(1<<16)));		//等待时间到达   
	SysTick->CTRL&=~SysTick_CTRL_ENABLE_Msk;	//关闭计数器
	SysTick->VAL =0X00;      					 //清空计数器	 
}

/*******************************************************************************
* 函 数 名         : delay_ms
* 函数功能		   : ms延时，
* 输    入         : nms：要延时的ms数
					注意:nms的值,SysTick->LOAD为24位寄存器，
					不要大于0xffffff*8*1000/SYSCLK
					对72M条件下,nms<=1864ms 
* 输    出         : 无
*******************************************************************************/
void delay_ms(u16 nms)
{	 		  	  
	u32 temp;		   
	SysTick->LOAD=(u32)nms*fac_ms;				//时间加载(SysTick->LOAD为24bit)
	SysTick->VAL =0x00;							//清空计数器
	SysTick->CTRL|=SysTick_CTRL_ENABLE_Msk ;	//开始倒数  
	do
	{
		temp=SysTick->CTRL;
	}while((temp&0x01)&&!(temp&(1<<16)));		//等待时间到达   
	SysTick->CTRL&=~SysTick_CTRL_ENABLE_Msk;	//关闭计数器
	SysTick->VAL =0X00;       					//清空计数器	  	    
} 
