#include "IndicatorLight.h"
#include "SysTick.h"
#include "usart1.h"
#include "usart3.h"
#include "iic.h"
#include "oled.h"
#include "adc.h"
#include "timer.h"


void All_Init()
{

    LED_Init();
    SysTick_Init(72);
    USART1_Init(115200);
	USART3_Init(9600);
    IIC_Init();
	OLED_Init();
	ADCx_Init();
	TIM4_Init(100,90-1);//¶¨Ê±100*90/72MHz=1/8KHz=125us
}

int main()
{
//    int i=0;
//	extern const unsigned char BMP1[];
//	unsigned char str1[]="12/01/19 13:19";
//	unsigned char str2[]="no GPS!";
    All_Init();
//	OLED_CLS();
	
    while(1)
    {
		while(!ADC_QUEUE_EMPTY())
		{
			USART1_WriteByte(ADC_POP_QUEUE());
		}
    }

}
