/**
 * Full Width Toggle Functionality
 * Toggles navigation and TOC visibility for full-width content view
 */

document.addEventListener('DOMContentLoaded', function() {
    // Wait for Material Design to initialize
    setTimeout(function() {
        createFullWidthToggle();
    }, 100);
});

function createFullWidthToggle() {
    // Check if button already exists
    if (document.getElementById('fullwidth-toggle')) {
        return;
    }

    // Create the toggle button
    const toggleButton = document.createElement('button');
    toggleButton.id = 'fullwidth-toggle';
    toggleButton.className = 'md-header__button md-icon';
    toggleButton.setAttribute("title", "Toggle Full Width View (Ctrl+Shift+F)")
    toggleButton.setAttribute('aria-label', 'Toggle Full Width View');
    
    // Button icon (fullscreen expand icon)
    toggleButton.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M5 5h5V3H3v7h2V5zm5 14H5v-5H3v7h7v-2zm9-14h-5V3h7v7h-2V5zm0 14v-5h2v7h-7v-2h5z"/>
        </svg>
    `;
    
    // Find the header options area (where palette toggle and search are)
    const headerOptions = document.querySelector('.md-header__option');
    
    if (headerOptions) {
        // Insert the button at the end of the header options
        headerOptions.appendChild(toggleButton);
    } else {
        console.warn('Could not find suitable location for full-width toggle button');
        return;
    }
    
    // Track current state
    let isFullWidth = false;
    
    // Get elements to toggle
    const navigation = document.querySelector('.md-sidebar--primary');
    const toc = document.querySelector('.md-sidebar--secondary');
    const content = document.querySelector('.md-content');
    const main = document.querySelector('.md-main');
    
    // Toggle function
    function toggleFullWidth() {
        isFullWidth = !isFullWidth;
        
        if (isFullWidth) {
          // Hide navigation and TOC
          if (navigation) {
            navigation.style.display = "none"
          }
          if (toc) {
            toc.style.display = "none"
          }

          // Expand content area
          if (content) {
            content.style.maxWidth = "none"
            content.style.margin = "0 auto"
            content.style.padding = "0 2rem"
          }

          if (main) {
            main.style.marginLeft = "0"
          }

          // Update button icon to exit fullscreen (compress icon - arrows pointing inward)
          toggleButton.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M14 14h5v2h-3v3h-2v-5zm-9 0v5h2v-3h3v-2H5zm5-9h2v3h3v2h-5V5zm-5 0v5h2V7h3V5H5z"/>
                </svg>
            `
          toggleButton.setAttribute("title", "Exit Full Width View (Ctrl+Shift+F)")

          // Add CSS class to body for additional styling
          document.body.classList.add("fullwidth-active")
        } else {
            // Show navigation and TOC
            if (navigation) {
                navigation.style.display = '';
            }
            if (toc) {
                toc.style.display = '';
            }
            
            // Reset content area
            if (content) {
                content.style.maxWidth = '';
                content.style.margin = '';
                content.style.padding = '';
            }
            
            if (main) {
                main.style.marginLeft = '';
            }
            
            // Update button icon to expand fullscreen
            toggleButton.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                    <path d="M5 5h5V3H3v7h2V5zm5 14H5v-5H3v7h7v-2zm9-14h-5V3h7v7h-2V5zm0 14v-5h2v7h-7v-2h5z"/>
                </svg>
            `;
            toggleButton.setAttribute("title", "Toggle Full Width View (Ctrl+Shift+F)")
            
            // Remove CSS class from body
            document.body.classList.remove('fullwidth-active');
        }
        
        // Store state in localStorage
        localStorage.setItem('mkdocs-fullwidth', isFullWidth.toString());
    }
    
    // Add click event listener
    toggleButton.addEventListener('click', toggleFullWidth);
    
    // Restore previous state from localStorage
    const savedState = localStorage.getItem('mkdocs-fullwidth');
    if (savedState === 'true') {
        toggleFullWidth();
    }
    
    // Handle keyboard shortcut (F11 alternative: Ctrl+Shift+F)
    document.addEventListener('keydown', function(event) {
        if (event.ctrlKey && event.shiftKey && event.key === 'F') {
            event.preventDefault();
            toggleFullWidth();
        }
    });
}
