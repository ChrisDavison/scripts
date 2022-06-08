package main

import (
	"fmt"
	"strings"
)

func main() {
	ftp := 259.0
	ftp_norm := ftp / 100.0
	weight := 74.0

	fmt.Printf("Cycling Power Zones at %.0fW FTP\n", ftp)
	fmt.Printf("    Recovery      %3.0f to %3.0fW\n", ftp_norm*0.0, ftp_norm*55.0)
	fmt.Printf("    Endurance     %3.0f to %3.0fW\n", ftp_norm*55.0, ftp_norm*75.0)
	fmt.Printf("    Sweetspot     %3.0f to %3.0fW\n", ftp_norm*75.0, ftp_norm*90.0)
	fmt.Printf("    Threshold     %3.0f to %3.0fW\n", ftp_norm*90.0, ftp_norm*105.0)
	fmt.Printf("    VO2Max        %3.0f to %3.0fW\n", ftp_norm*105.0, ftp_norm*120.0)
	fmt.Printf("    Anaerobic     %3.0f to %3.0fW\n", ftp_norm*120.0, ftp_norm*150.0)
	fmt.Printf("    Neuromuscular >%vW\n", ftp_norm*150/100)
	fmt.Printf("\nTheoretical W/kg\n")
	fmt.Printf("    NOW %.1f W/kg\n", ftp/weight)
	fmt.Printf("    for 4   W/kg, %.0fW\n", 4*weight)
	fmt.Printf("    for 3.5 W/kg, %.0fW\n", 3.5*weight)
	fmt.Printf("    for 3   W/kg, %.0fW\n", 3*weight)
	strings.Join([]string{}, "")
}
