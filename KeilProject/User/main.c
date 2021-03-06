#include "IndicatorLight.h"
#include "SysTick.h"
#include "usart1.h"
#include "usart2.h"

#include "adc.h"
#include "timer.h"


void All_Init()
{

    LED_Init();
    SysTick_Init(72);
    USART1_Init(115200);
	USART2_Init(115200);
	ADCx_Init();
	TIM4_Init(100,90-1);//��ʱ100*90/72MHz=1/8KHz=125us
}

int main()
{
	uint8_t temp;
	uint8_t i=0;
    All_Init();	
    while(1)
    {
		while(!ADC_QUEUE_EMPTY())
		{
			temp = ADC_POP_QUEUE();
			USART1_WriteByte(temp);
			//USART2_WriteByte(temp);
			i++;
			if(i%10==0)
			{
				led=~led;
			}
		}
    }

}
