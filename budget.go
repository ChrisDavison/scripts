package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

// Finance represents either an outgoing or incoming monetary amount
type Finance struct {
	Name  string
	Value float64
}

type categorisedFinances map[string][]Finance

func (f Finance) String() string {
	return fmt.Sprintf("%-15v £%v", f.Name, f.Value)
}

func isDashLine(line string) bool {
	return line == strings.Repeat("-", len(line))
}

func display(wage, savings Finance, categorisedFinances map[string][]Finance) {
	fmt.Println("====== BASELINE ======")
	fmt.Println(wage)
	fmt.Println(savings)
	fmt.Println()
	fmt.Println("====== COSTS ======")
	for category, finances := range categorisedFinances {
		sum := 0.0
		for _, finance := range finances {
			sum += finance.Value
		}
		fmt.Println(Finance{category, sum})
	}
}

func parseFinances(filename string) (savings, wage Finance, finances categorisedFinances) {
	var costs []Finance
	categorisedCosts := make(map[string][]Finance)
	var current string

	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	filebuffer := bufio.NewScanner(file)

	for filebuffer.Scan() {
		line := filebuffer.Text()
		if len(line) == 0 || isDashLine(line) {
			continue
		} else if strings.HasPrefix(line, "Income") {
			value, _ := strconv.ParseFloat(strings.Split(line, " -- £")[1], 64)
			wage = Finance{"Income", value}
		} else if strings.HasPrefix(line, "Savings") {
			value, _ := strconv.ParseFloat(strings.Split(line, " -- £")[1], 64)
			savings = Finance{"Savings", value}
		} else if strings.Contains(line, " -- £") {
			parts := strings.Split(line, " -- £")
			value, _ := strconv.ParseFloat(parts[1], 64)
			costs = append(costs, Finance{parts[0], value})
		} else {
			if len(costs) > 0 {
				categorisedCosts[current] = costs
			}
			current = line
			costs = []Finance{}
		}
	}
	if len(costs) > 0 {
		categorisedCosts[current] = costs
	}
	return savings, wage, categorisedCosts
}

func main() {
	fnBudget := os.Getenv("BUDGET")
	savings, wage, categorisedCosts := parseFinances(fnBudget)
	display(wage, savings, categorisedCosts)
}
