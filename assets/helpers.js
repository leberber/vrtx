window.dash_clientside = Object.assign({}, window.dash_clientside, {
    helpers: {
        hide_show_sidebar: function (maximize_action) {
            if (maximize_action % 2 === 0) {
                console.log(maximize_action);
                // Sidebar is hidden (width reduced to 0) with smooth transition
                return [
                    {
                        'width': '0px',  // Corrected from 'display' to 'width'
                        'overflow': 'hidden', 
                        'transition': 'width 0.5s ease-in-out', 
                        'position': 'fixed',
                        // 'border': '2px solid green', 
                    },  
                    {
                        'marginLeft': '0px', 
                        'transition': 'margin-left 0.5s ease-in-out', 
                        // 'border': '2px solid red',
                        'height':'100vh'
                    }
                ];
            }
            // Sidebar is shown (width expanded) with smooth transition
            return [
                {
                    'width': '300px',  // Sidebar width set to 200px
                    'transition': 'width 0.5s ease-in-out',  
                    'position': 'fixed',
                    // 'border': '2px solid green', 
                },  
                {
                    'marginLeft': '300px',  // Main content adjusts its margin for the sidebar
                    'transition': 'margin-left 0.5s ease-in-out', 
                    // 'border': '2px solid red',
                    'height':'100vh'
                }
            ];
        },
    },
});
