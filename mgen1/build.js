const fs = require('fs');
const path = require('path');

// Read build.json
const buildConfig = JSON.parse(fs.readFileSync('build.json', 'utf-8'));

// Create dist directory if it doesn't exist
const distDir = path.join(__dirname, 'public/dist');
if (!fs.existsSync(distDir)) {
    fs.mkdirSync(distDir, { recursive: true });
}

// Bundle JS files
Object.entries(buildConfig).forEach(([output, inputs]) => {
    const outputPath = path.join(distDir, output);
    const outputDir = path.dirname(outputPath);
    
    // Create output directory if it doesn't exist
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    
    // Concatenate all input files
    const content = inputs.map(input => {
        const inputPath = path.join(__dirname, input);
        return fs.readFileSync(inputPath, 'utf-8');
    }).join('\n');
    
    // Write to output file
    fs.writeFileSync(outputPath, content);
});
