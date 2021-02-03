Import-Module .\Invoke-PSImage.ps1
Start-Transcript -Path "execution_log"

$cluster_number = 5000
$counter_mode1_obfuscated = 0
$counter_mode1_deobfuscated = 0

$counter_1024x1024_obfuscated = 0
$counter_1024x1024_deobfuscated = 0
$counter_512x512_obfuscated = 0
$counter_512x512_deobfuscated = 0
$counter_256x256_obfuscated = 0
$counter_256x256_deobfuscated = 0

# Creation of the Mode-1 directory structure
New-Item .\images\mode-1 -ItemType directory 
New-Item .\images\mode-1\obfuscated -ItemType directory
New-Item .\images\mode-1\deobfuscated -ItemType directory

# Creation of the Mode-2 directory structure
New-Item .\images\mode-2 -ItemType directory
New-Item .\images\mode-2\clean -ItemType directory
New-Item .\images\mode-2\clean\1024x1024 -ItemType directory
New-Item .\images\mode-2\clean\1024x1024\png -ItemType directory
New-Item .\images\mode-2\clean\1024x1024\jpg -ItemType directory
New-Item .\images\mode-2\clean\512x512 -ItemType directory
New-Item .\images\mode-2\clean\512x512\png -ItemType directory
New-Item .\images\mode-2\clean\512x512\jpg -ItemType directory
New-Item .\images\mode-2\clean\256x256 -ItemType directory
New-Item .\images\mode-2\clean\256x256\png -ItemType directory
New-Item .\images\mode-2\clean\256x256\jpg -ItemType directory
New-Item .\images\mode-2\obfuscated -ItemType directory
New-Item .\images\mode-2\obfuscated\1024x1024 -ItemType directory
New-Item .\images\mode-2\obfuscated\512x512 -ItemType directory
New-Item .\images\mode-2\obfuscated\256x256 -ItemType directory
New-Item .\images\mode-2\deobfuscated -ItemType directory
New-Item .\images\mode-2\deobfuscated\1024x1024 -ItemType directory
New-Item .\images\mode-2\deobfuscated\512x512 -ItemType directory
New-Item .\images\mode-2\deobfuscated\256x256 -ItemType directory

# Catch all Scripts
$deobfuscated_scripts = Get-ChildItem ".\scripts\deobfuscated"
$obfuscated_scripts = Get-ChildItem ".\scripts\obfuscated"

# Catch all images, which can be used for injection
$1024x1024_pictures = Get-ChildItem ".\1024x1024"
$512x512_pictures = Get-ChildItem ".\512x512"
$256x256_pictures = Get-ChildItem ".\256x256"

# Catch the target for saving the images of the set in mode-1
$mode1_obfuscated_images = ".\images\mode-1\obfuscated"
$mode1_deobfuscated_images = ".\images\mode-1\deobfuscated"

# Catch the target for saving the images of the set in mode-2
$clean_images_1024x1024_png = ".\images\mode-2\clean\1024x1024\png"
$clean_images_1024x1024_jpg = ".\images\mode-2\clean\1024x1024\jpg"
$obfuscated_images_1024x1024 = ".\images\mode-2\obfuscated\1024x1024"
$deobfuscated_images_1024x1024 = ".\images\mode-2\deobfuscated\1024x1024"

$clean_images_512x512_png = ".\images\mode-2\clean\512x512\png"
$clean_images_512x512_jpg = ".\images\mode-2\clean\512x512\jpg"
$obfuscated_images_512x512 = ".\images\mode-2\obfuscated\512x512"
$deobfuscated_images_512x512 = ".\images\mode-2\deobfuscated\512x512"

$clean_images_256x256_png = ".\images\mode-2\clean\256x256\png"
$clean_images_256x256_jpg = ".\images\mode-2\clean\256x256\jpg"
$obfuscated_images_256x256 = ".\images\mode-2\obfuscated\256x256"
$deobfuscated_images_256x256 = ".\images\mode-2\deobfuscated\256x256"

"Injected File;Script;Script Size in Bytes" | Out-File -Append "deob_mode1.csv" -Encoding UTF8
"Injected File;Script;Script Size in Bytes" | Out-File -Append "ob_mode1.csv" -Encoding UTF8

"Injected File;Script;Script Size in Bytes" | Out-File -Append "1024x1024_deob_mode2.csv" -Encoding UTF8
"Injected File;Script;Script Size in Bytes" | Out-File -Append "512x512_deob_mode2.csv" -Encoding UTF8
"Injected File;Script;Script Size in Bytes" | Out-File -Append "256x256_deob_mode2.csv" -Encoding UTF8

"Injected File;Script;Script Size in Bytes" | Out-File -Append "1024x1024_ob_mode2.csv" -Encoding UTF8
"Injected File;Script;Script Size in Bytes" | Out-File -Append "512x512_ob_mode2.csv" -Encoding UTF8
"Injected File;Script;Script Size in Bytes" | Out-File -Append "256x256_ob_mode2.csv" -Encoding UTF8

echo ("")
echo ("")
echo ("========== START MODE-1 INJECTION DEOBFUSCATED ==========")
for($s = 0; $s -lt $deobfuscated_scripts.Count; $s++){
    echo ("File: " + $s + "/" + $deobfuscated_scripts.Count)

    # Creation of the Name for the new file
    $new_file_mode1_deobfuscated = $mode1_deobfuscated_images + "\" + $deobfuscated_scripts[$s]
    $new_file_mode1_deobfuscated = $new_file_mode1_deobfuscated.Replace(".asd", ".png")
    
    Invoke-PSImage -Script $deobfuscated_scripts[$s].FullName -Out $new_file_mode1_deobfuscated > $null
    $counter_mode1_deobfuscated++
    echo ("Script " + $deobfuscated_scripts[$s].FullName + " injected: " + $new_file_mode1_deobfuscated + " written.")
    echo ("")

    $deobfuscated_scripts[$s].Name.Replace(".asd", ".png")+";"+$deobfuscated_scripts[$s].Name.Replace(".asd", "")+";"+$deobfuscated_scripts[$s].Length | Out-File -Append "deob_mode1.csv" -Encoding UTF8

}

echo ("========== FINISHED MODE-1 INJECTION DEOBFUSCATED ==========")
echo ("Number deobfuscated images: " + $counter_mode1_deobfuscated)

echo ("")
echo ("")
echo ("========== START MODE-1 INJECTION OBFUSCATED ==========")
for($s = 0; $s -lt $obfuscated_scripts.Count; $s++){
    echo ("File: " + $s + "/" + $obfuscated_scripts.Count)

    # Creation of the Name for the new file
    $new_file_mode1_obfuscated = $mode1_obfuscated_images + "\" + $obfuscated_scripts[$s]
    $new_file_mode1_obfuscated = $new_file_mode1_obfuscated.Replace(".asd", ".png")
    
    Invoke-PSImage -Script $obfuscated_scripts[$s].FullName -Out $new_file_mode1_obfuscated > $null
    $counter_mode1_obfuscated++
    echo ("Script " + $obfuscated_scripts[$s].FullName + " injected: " + $new_file_mode1_obfuscated + " written.")
    echo ("")

    $obfuscated_scripts[$s].Name.Replace(".asd", ".png")+";"+$obfuscated_scripts[$s].Name.Replace(".asd", "")+";"+$obfuscated_scripts[$s].Length | Out-File -Append "ob_mode1.csv" -Encoding UTF8

}
echo ("========== FINISHED MODE-1 INJECTION OBFUSCATED ==========")
echo ("Number obfuscated images: " + $counter_mode1_obfuscated)

echo ("")
echo ("")
echo ("========== START MODE-2 INJECTION INTO 1024x1024 IMAGES ==========")
for($y = 0; $y -lt $cluster_number; $y++){

    echo ("File: " + $y + "/" + $cluster_number)
    
    $new_file_obfuscated = $obfuscated_images_1024x1024 + "\" + $1024x1024_pictures[$y]
    $new_file_obfuscated = $new_file_obfuscated.Replace(".jpg", ".png")
        
    $new_file_deobfuscated = $deobfuscated_images_1024x1024 + "\" + $1024x1024_pictures[$y]
    $new_file_deobfuscated = $new_file_deobfuscated.Replace(".jpg", ".png")
        
    $new_file_converted = $clean_images_1024x1024_png + "\" + $1024x1024_pictures[$y]
    $new_file_converted = $new_file_converted.Replace(".jpg", ".png")

    # Try to create obfuscated picture
    Invoke-PSImage -Script $obfuscated_scripts[$y % $obfuscated_scripts.Count].FullName -Out $new_file_obfuscated -Image $1024x1024_pictures[$y].FullName > $null
    echo ("Script " + $obfuscated_scripts[$y % $obfuscated_scripts.Count].FullName + " into " + $1024x1024_pictures[$y].FullName + " injected: " + $new_file_obfuscated + " written.")
    $counter_1024x1024_obfuscated++
        
    # Try to create deobfuscated picture
    Invoke-PSImage -Script $deobfuscated_scripts[$y % $deobfuscated_scripts.Count].FullName -Out $new_file_deobfuscated -Image $1024x1024_pictures[$y].FullName > $null
    echo ("Script " + $deobfuscated_scripts[$y % $deobfuscated_scripts.Count].FullName + " into " + $1024x1024_pictures[$y].FullName + " injected: " + $new_file_deobfuscated + " written.")
    $counter_1024x1024_deobfuscated++
        
    # Convert jpg to png
    magick convert $1024x1024_pictures[$y].FullName PNG24:$new_file_converted > $null
    echo ("Clean Picture " + $1024x1024_pictures[$y].FullName + " converted to " + $new_file_converted + ".")
        
    # Copy clean image to set
    Copy-Item $1024x1024_pictures[$y].FullName -Destination $clean_images_1024x1024_jpg
    echo ("Clean Picture " + $1024x1024_pictures[$y].FullName + " copied to " + $clean_images_1024x1024_jpg + ".")
    echo ("")

    $1024x1024_pictures[$y].Name.Replace(".jpg", ".png")+";"+$deobfuscated_scripts[$y % $deobfuscated_scripts.Count].Name.Replace(".asd", "")+";"+$deobfuscated_scripts[$y % $deobfuscated_scripts.Count].Length | Out-File -Append "1024x1024_deob_mode2.csv" -Encoding UTF8
    $1024x1024_pictures[$y].Name.Replace(".jpg", ".png")+";"+$obfuscated_scripts[$y % $obfuscated_scripts.Count].Name.Replace(".asd", "")+";"+$obfuscated_scripts[$y % $obfuscated_scripts.Count].Length | Out-File -Append "1024x1024_ob_mode2.csv" -Encoding UTF8


}

echo ("========== FINISHED MODE-2 INJECTION INTO 1024x1024 IMAGES ==========")
echo ("Number obfuscated images: " + $counter_1024x1024_obfuscated)
echo ("Number deobfuscated images: " + $counter_1024x1024_deobfuscated)

echo ("COMPARISON OF ALL 1024x1024 FILES:")
$dir1 = Get-ChildItem $clean_images_1024x1024_jpg
$dir2 = Get-ChildItem $clean_images_1024x1024_png
$dir3 = Get-ChildItem $obfuscated_images_1024x1024
$dir4 = Get-ChildItem $deobfuscated_images_1024x1024

$failures = 0
for($k = 0; $k -lt $cluster_number; $k++){
    if($dir1[$k].Name.Replace(".jpg", ".png") -ne $dir2[$k].Name){
        echo ($dir1[$k].Name + " (.images\clean\1024x1024\jpg) is not equals " + $dir2[$k].Name + " (.images\clean\1024x1024\png)!")
        $failures++
    }

    if($dir1[$k].Name.Replace(".jpg", ".png") -ne $dir3[$k].Name){
        echo ($dir1[$k].Name + " (.images\clean\1024x1024\jpg) is not equals " + $dir3[$k].Name + " (.images\obfuscated\1024x1024)!")
        $failures++
    }

    if($dir1[$k].Name.Replace(".jpg", ".png") -ne $dir4[$k].Name){
        echo ($dir1[$k].Name + " (.images\clean\1024x1024\jpg) is not equals " + $dir4[$k].Name + " (.images\deobfuscated\1024x1024)!")
        $failures++
    }

}
if($failures -ne 0){
    echo ("Different files in 1024x1024 set detected => Set is not guilty!")
}else{
    echo ("No differences in 1024x1024 set detected => Set guilty!")
}


echo ("")
echo ("")
echo ("========== START MODE-2 INJECTION INTO 512x512 IMAGES ==========")
for($y = 0; $y -lt $cluster_number; $y++){

    echo ("File: " + $y + "/" + $cluster_number)

    # Creation of the Name for the new file
    $new_file_obfuscated = $obfuscated_images_512x512 + "\" + $512x512_pictures[$y]
    $new_file_obfuscated = $new_file_obfuscated.Replace(".jpg", ".png")
        
    $new_file_deobfuscated = $deobfuscated_images_512x512 + "\" + $512x512_pictures[$y]
    $new_file_deobfuscated = $new_file_deobfuscated.Replace(".jpg", ".png")

    $new_file_converted = $clean_images_512x512_png + "\" + $512x512_pictures[$y]
    $new_file_converted = $new_file_converted.Replace(".jpg", ".png")

    # Try to create obfuscated picture
    Invoke-PSImage -Script $obfuscated_scripts[$y % $obfuscated_scripts.Count].FullName -Out $new_file_obfuscated -Image $512x512_pictures[$y].FullName > $null
    echo ("Script " + $obfuscated_scripts[$y % $obfuscated_scripts.Count].FullName + " into " + $512x512_pictures[$y].FullName + " injected: " + $new_file_obfuscated + " written.")
    $counter_512x512_obfuscated++
        
    # Try to create deobfuscated picture
    Invoke-PSImage -Script $deobfuscated_scripts[$y % $deobfuscated_scripts.Count].FullName -Out $new_file_deobfuscated -Image $512x512_pictures[$y].FullName > $null
    echo ("Script " + $deobfuscated_scripts[$y % $deobfuscated_scripts.Count].FullName + " into " + $512x512_pictures[$y].FullName + " injected: " + $new_file_deobfuscated + " written.")
    $counter_512x512_deobfuscated++
        
    # Convert jpg to png
    magick convert $512x512_pictures[$y].FullName PNG24:$new_file_converted > $null
    echo ("Clean Picture " + $512x512_pictures[$y].FullName + " converted to " + $new_file_converted + ".")

    # Copy clean image to set
    Copy-Item $512x512_pictures[$y].FullName -Destination $clean_images_512x512_jpg
    echo ("Clean Picture " + $512x512_pictures[$y].FullName + " copied to " + $clean_images_512x512_jpg + ".")
    echo ("")
    
    $512x512_pictures[$y].Name.Replace(".jpg", ".png")+";"+$deobfuscated_scripts[$y % $deobfuscated_scripts.Count].Name.Replace(".asd", "")+";"+$deobfuscated_scripts[$y % $deobfuscated_scripts.Count].Length | Out-File -Append "512x512_deob_mode2.csv" -Encoding UTF8
    $512x512_pictures[$y].Name.Replace(".jpg", ".png")+";"+$obfuscated_scripts[$y % $obfuscated_scripts.Count].Name.Replace(".asd", "")+";"+$obfuscated_scripts[$y % $obfuscated_scripts.Count].Length | Out-File -Append "512x512_ob_mode2.csv" -Encoding UTF8

}
echo ("========== FINISHED MODE-2 INJECTION INTO 512x512 IMAGES ==========")
echo ("Number obfuscated images: " + $counter_512x512_obfuscated)
echo ("Number deobfuscated images: " + $counter_512x512_deobfuscated)

echo ("COMPARISON OF ALL 512x512 FILES:")
$dir1 = Get-ChildItem $clean_images_512x512_jpg
$dir2 = Get-ChildItem $clean_images_512x512_png
$dir3 = Get-ChildItem $obfuscated_images_512x512
$dir4 = Get-ChildItem $deobfuscated_images_512x512

$failures = 0
for($k = 0; $k -lt $cluster_number; $k++){
    if($dir1[$k].Name.Replace(".jpg", ".png") -ne $dir2[$k].Name){
        echo ($dir1[$k].Name + " (.images\clean\512x512\jpg) is not equals " + $dir2[$k].Name + " (.images\clean\512x512\png)!")
        $failures++
    }

    if($dir1[$k].Name.Replace(".jpg", ".png") -ne $dir3[$k].Name){
        echo ($dir1[$k].Name + " (.images\clean\512x512\jpg) is not equals " + $dir3[$k].Name + " (.images\obfuscated\512x512)!")
        $failures++
    }

    if($dir1[$k].Name.Replace(".jpg", ".png") -ne $dir4[$k].Name){
        echo ($dir1[$k].Name + " (.images\clean\512x512\jpg) is not equals " + $dir4[$k].Name + " (.images\deobfuscated\512x512)!")
        $failures++
    }
}
if($failures -ne 0){
    echo ("Different files in 512x512 set detected => Set is not guilty!")
}else{
    echo ("No differences in 512x512 set detected => Set guilty!")
}

echo ("")
echo ("")
echo ("========== START MODE-2 INJECTION INTO 256x256 IMAGES ==========")
for($y = 0; $y -lt $cluster_number; $y++){
    
    echo ("File: " + $y + "/" + $cluster_number)

    $new_file_obfuscated = $obfuscated_images_256x256 + "\" + $256x256_pictures[$y]
    $new_file_obfuscated = $new_file_obfuscated.Replace(".jpg", ".png")

    $new_file_deobfuscated = $deobfuscated_images_256x256 + "\" + $256x256_pictures[$y]
    $new_file_deobfuscated = $new_file_deobfuscated.Replace(".jpg", ".png")

    $new_file_converted = $clean_images_256x256_png + "\" + $256x256_pictures[$y]
    $new_file_converted = $new_file_converted.Replace(".jpg", ".png")
    
    Invoke-PSImage -Script $obfuscated_scripts[$y % $obfuscated_scripts.Count].FullName -Out $new_file_obfuscated -Image $256x256_pictures[$y].FullName > $null
    echo ("Script " + $obfuscated_scripts[$y % $obfuscated_scripts.Count].FullName + " into " + $256x256_pictures[$y].FullName + " injected: " + $new_file_obfuscated + " written.")
    $counter_256x256_obfuscated++

    Invoke-PSImage -Script $deobfuscated_scripts[$y % $deobfuscated_scripts.Count].FullName -Out $new_file_deobfuscated -Image $256x256_pictures[$y].FullName > $null
    echo ("Script " + $deobfuscated_scripts[$y % $deobfuscated_scripts.Count].FullName + " into " + $256x256_pictures[$y].FullName + " injected: " + $new_file_deobfuscated + " written.")
    $counter_256x256_deobfuscated++

    magick convert $256x256_pictures[$y].FullName PNG24:$new_file_converted > $null
    echo ("Clean Picture " + $256x256_pictures[$y].FullName + " converted to " + $new_file_converted + ".")

    Copy-Item $256x256_pictures[$y].FullName -Destination $clean_images_256x256_jpg
    echo ("Clean Picture " + $256x256_pictures[$y].FullName + " copied to " + $clean_images_256x256_jpg + ".")
    echo ("")
    
    $256x256_pictures[$y].Name.Replace(".jpg", ".png")+";"+$deobfuscated_scripts[$y % $deobfuscated_scripts.Count].Name.Replace(".asd", "")+";"+$deobfuscated_scripts[$y % $deobfuscated_scripts.Count].Length | Out-File -Append "256x256_deob_mode2.csv" -Encoding UTF8
    $256x256_pictures[$y].Name.Replace(".jpg", ".png")+";"+$obfuscated_scripts[$y % $obfuscated_scripts.Count].Name.Replace(".asd", "")+";"+$obfuscated_scripts[$y % $obfuscated_scripts.Count].Length | Out-File -Append "256x256_ob_mode2.csv" -Encoding UTF8

}
echo ("========== FINISHED MODE-2 INJECTION INTO 256x256 IMAGES ==========")
echo ("Number obfuscated images: " + $counter_256x256_obfuscated)
echo ("Number deobfuscated images: " + $counter_256x256_deobfuscated)

echo ("COMPARISON OF ALL 256x256 FILES:")
$dir1 = Get-ChildItem $clean_images_256x256_jpg
$dir2 = Get-ChildItem $clean_images_256x256_png
$dir3 = Get-ChildItem $obfuscated_images_256x256
$dir4 = Get-ChildItem $deobfuscated_images_256x256

$failures = 0
for($k = 0; $k -lt $cluster_number; $k++){
    if($dir1[$k].Name.Replace(".jpg", ".png") -ne $dir2[$k].Name){
        echo ($dir1[$k].Name + " (.images\clean\256x256\jpg) is not equals " + $dir2[$k].Name + " (.images\clean\256x256\png)!")
        $failures++
    }

    if($dir1[$k].Name.Replace(".jpg", ".png") -ne $dir3[$k].Name){
        echo ($dir1[$k].Name + " (.images\clean\256x256\jpg) is not equals " + $dir3[$k].Name + " (.images\obfuscated\256x256)!")
        $failures++
    }

    if($dir1[$k].Name.Replace(".jpg", ".png") -ne $dir4[$k].Name){
        echo ($dir1[$k].Name + " (.images\clean\256x256\jpg) is not equals " + $dir4[$k].Name + " (.images\deobfuscated\256x256)!")
        $failures++
    }
}
if($failures -ne 0){
    echo ("Different files in 256x256 set detected => Set is not guilty!")
}else{
    echo ("No differences in 256x256 set detected => Set guilty!")
}
