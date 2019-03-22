#include "IndicatorLight.h"
#include "SysTick.h"
#include "usart1.h"
#include "adc.h"
#include "timer.h"


void All_Init()
{

    LED_Init();
    SysTick_Init(72);
    USART1_Init(115200);
	ADCx_Init();
	TIM4_Init(100,90-1);//¶¨Ê±100*90/72MHz=1/8KHz=125us
}

int main()
{

    All_Init();	
    while(1)
    {
		while(!ADC_QUEUE_EMPTY())
		{
			USART1_WriteByte(ADC_POP_QUEUE());
		}
    }

}
