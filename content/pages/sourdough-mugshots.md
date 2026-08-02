Title: Sourdough mugshots.
slug: sourdough-mugshots
save_as: sourdough-mugshots.html
Description: Every sourdough I have baked, in mugshot format.

<style>
.sourdough-wrapper {
    width: 100%;
    max-width: 600px;
    margin: -100px auto 0 auto;
    text-align: center;
}

/* The Background & Height Chart */
.sourdough-mugshot-container {
    position: relative;
    aspect-ratio: 0.9;
    overflow: hidden;
    border: 6px solid #111; /* Thick, stark border */
    background-color: #ededed; /* Institutional grey wall */
    
    /* Draws the height chart lines behind the bread */
    background-image:
        /* Minor lines (every 20px) */
        repeating-linear-gradient(to bottom, transparent, transparent 19px, rgba(0,0,0,0.1) 19px, rgba(0,0,0,0.1) 20px),
        /* Major lines (every 100px) */
        repeating-linear-gradient(to bottom, transparent, transparent 99px, rgba(0,0,0,0.4) 99px, rgba(0,0,0,0.4) 100px);
    
    /* Sets up flexbox to perfectly center the placard at the bottom */
    display: flex;
    justify-content: center;
    align-items: flex-end;
}

/* The Bread Image */
.sourdough-mugshot-container img {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    z-index: 1;
    
    /* Adds a harsh "camera flash" drop shadow and slightly boosts contrast */
    filter: contrast(1.1) drop-shadow(0 15px 25px rgba(0,0,0,0.4));
}

/* The Suspect Board */
.mugshot-placard {
    position: relative;
    z-index: 2;
    background: #111;
    color: #fff;
    font-family: 'Syne Mono', monospace; /* Uses your theme's typewriter font */
    text-align: center;
    width: 75%;
    margin-bottom: 5px; /* Floats it just above the bottom edge */
    
    /* Creates the classic white inner-border look */
    border: 2px solid #fff;
    outline: 6px solid #111;
    /*padding: 10px 15px;*/
    box-shadow: 2px 10px 20px rgba(0,0,0,0.5);
}

.placard-header, 
.placard-id {
    font-size: 0.75rem;
    letter-spacing: 2px;
    color: #aaa;
    margin: 0;
}

.loaf-date {
    font-size: 1.6rem;
    margin: 5px 0;
    letter-spacing: 1px;
    font-weight: bold;
    color: #fff;
}


@media (max-width: 768px) {
    .sourdough-wrapper {
        width: 100%;
        max-width: 500px;
        margin: 0 auto 0 auto;
        text-align: center;
    }
}
</style>

<div class="sourdough-wrapper">
    <div class="sourdough-mugshot-container">
        
        <!-- The Bread -->
        <img id="loaf-frame" src="/images/sourdough-mugshots/20251109.png" alt="Sourdough Crumb Evolution">
        
        <!-- The Suspect Placard -->
        <div class="mugshot-placard">
            <h3 id="loaf-date-display" class="loaf-date">NOVEMBER 11, 2025</h3>
        </div>

    </div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
    // 1. Array of your stabilized PNGs (in chronological order)
    const mugshots = [
        "20200608",
        "20201027",
        "20210103",
        "20210310",
        "20210524",
        "20210719",
        "20210926",
        "20211115",
        "20220318",
        "20220411",
        "20220502",
        "20220529",
        "20220814",
        "20221113-2",
        "20221113",
        "20221119",
        "20221220",
        "20230326",
        "20230522",
        "20230807",
        "20240219",
        "20240428",
        "20250126",
        "20250309",
        "20251109"
    ];

    const basePath = "/images/sourdough-mugshots/";

// Preload images to prevent flickering
    mugshots.forEach(dateStr => {
        const img = new Image();
        img.src = `${basePath}${dateStr}.png`;
    });

    const imgElement = document.getElementById('loaf-frame');
    const dateElement = document.getElementById('loaf-date-display');
    let currentFrame = 0;

    // Helper function to turn "20200608" into "June 8, 2020"
    function formatMugshotDate(dateString) {
        const year = dateString.substring(0, 4);
        // JavaScript months are 0-indexed (0 = Jan, 11 = Dec), so we subtract 1
        const month = parseInt(dateString.substring(4, 6), 10) - 1; 
        const day = dateString.substring(6, 8);
        
        const dateObj = new Date(year, month, day);
        
        // toLocaleDateString automatically handles beautiful, readable formatting
        return dateObj.toLocaleDateString('en-US', { 
            month: 'long', 
            day: 'numeric', 
            year: 'numeric' 
        });
    }

    // The Animation Loop
    setInterval(() => {
        currentFrame = (currentFrame + 1) % mugshots.length;
        const activeDateString = mugshots[currentFrame];
        
        // Update the image source
        imgElement.src = `${basePath}${activeDateString}.png`;
        
        // Update the date text beneath it
        dateElement.textContent = formatMugshotDate(activeDateString);
        
    }, 1000); // Swaps every 1000ms (1 second). Adjust to taste!
});
</script>
