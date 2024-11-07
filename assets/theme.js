window.dash_clientside = Object.assign({}, window.dash_clientside, {
   
    theme: {

         theme_switcher_callback: function (value) {
          console.log(value)
            
            let lightIcon = {'props': {'icon': 'ic:baseline-light-mode', 'width': 40, 'color':'gold'}, 'type': 'DashIconify', 'namespace': 'dash_iconify'}
            let darkIcon = {'props': {'icon': 'ic:sharp-dark-mode', 'width': 40, 'color':'#e8e3e6'}, 'type': 'DashIconify', 'namespace': 'dash_iconify'}
            let custom_theme_colors = {
                "dark_blue": ["#4A5468","#465064","#424C60","#3E485B","#3A4457","#354053","#313C4F","#2D384A","#293446","#253042"],
                "dimmed_purple":[ "#F5F2F6","#E6DEEA", "#DAC9E1", "#CFB3DB", "#C1A6CD", "#B39ABE", "#A790B0", "#9A87A3","#8F7E96","#85778B" ],
                'vp':[
                    "#9989A7",
                    "#8A749F",
                    "#7C5F98",
                    "#70508F",
                    "#654188",
                    "#5B3283",
                    "#52247F",
                    "#492869",
                    "#492869",
                    "#492869",
                  ]
               }
            let lightColorScheme =  { 
                "fontFamily": "'Roboto','Arial',sans-serif",
                "colorScheme": "light",
                "colors":custom_theme_colors,
                "components": {
                },
            }
            
            let darktColorScheme =  { 
                "colorScheme": "dark",
                "fontFamily": "'YouTube Sans','Roboto',sans-serif",
                "colors": custom_theme_colors,
                "components": {
                },
            }

            if (value ==='Light') { 
                const style = document.createElement('style');

                document.head.appendChild(style);
                document.documentElement.style.setProperty('--theme-background', 'white');
                document.documentElement.style.setProperty('--theme-background-darker', 'white');
                document.documentElement.style.setProperty('--shadow-dk', 'rgba(219, 166, 232, 0.1) 0px 3px 12px');

               return [lightColorScheme, 'light']
            } 
            
               const style = document.createElement('style');
       
              document.head.appendChild(style);
              document.documentElement.style.setProperty('--theme-background', '#2e2e2e');
              document.documentElement.style.setProperty('--theme-background-darker', 'rgb(31, 31, 31)');
              document.documentElement.style.setProperty('--shadow-dk', 'none');   

        return [ darktColorScheme, 'dark']
        }
  
    },
});

