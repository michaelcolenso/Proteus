#!/bin/bash
# Quick CV Generation Script
# Compiles different CV variants for various job applications

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to compile and show status
compile_cv() {
    local variant=$1
    local description=$2

    echo -e "${BLUE}Compiling ${variant}...${NC}"
    if typst compile "${variant}.typ" "${variant}.pdf"; then
        echo -e "${GREEN}✓ ${description} compiled successfully${NC}"
        echo -e "  Output: ${variant}.pdf"
        return 0
    else
        echo -e "${YELLOW}✗ Failed to compile ${variant}${NC}"
        return 1
    fi
}

# Main script
case $1 in
    "senior-pm")
        echo "=== Generating Senior PM CV ==="
        compile_cv "cv_senior_pm" "Senior Project Manager CV"
        ;;

    "superintendent")
        echo "=== Generating Superintendent CV ==="
        compile_cv "cv_superintendent" "Superintendent CV"
        ;;

    "estimator")
        echo "=== Generating Estimator CV ==="
        compile_cv "cv_estimator" "Estimator/Preconstruction CV"
        ;;

    "exec-summary")
        echo "=== Generating Executive Summary CV ==="
        compile_cv "cv_exec_summary" "One-Page Executive Summary"
        ;;

    "standard")
        echo "=== Generating Standard CV ==="
        compile_cv "cv" "Standard CV"
        ;;

    "letter")
        echo "=== Generating Cover Letter ==="
        echo -e "${BLUE}Compiling letter.typ...${NC}"
        if typst compile letter.typ letter.pdf; then
            echo -e "${GREEN}✓ Cover letter compiled successfully${NC}"
            echo -e "  Output: letter.pdf"
        else
            echo -e "${YELLOW}✗ Failed to compile cover letter${NC}"
        fi
        ;;

    "all")
        echo "=== Generating All CV Variants ==="
        echo ""

        compile_cv "cv" "Standard CV"
        echo ""

        compile_cv "cv_senior_pm" "Senior PM CV"
        echo ""

        compile_cv "cv_superintendent" "Superintendent CV"
        echo ""

        compile_cv "cv_estimator" "Estimator CV"
        echo ""

        compile_cv "cv_exec_summary" "Executive Summary"
        echo ""

        echo -e "${BLUE}Compiling cover letter...${NC}"
        if typst compile letter.typ letter.pdf; then
            echo -e "${GREEN}✓ Cover letter compiled${NC}"
        fi

        echo ""
        echo -e "${GREEN}=== All variants compiled ===${NC}"
        echo "Check the root directory for PDF outputs"
        ;;

    "clean")
        echo "=== Cleaning compiled PDFs ==="
        rm -f cv.pdf cv_*.pdf letter.pdf
        echo -e "${GREEN}✓ Cleaned all PDF files${NC}"
        ;;

    "watch")
        if [ -z "$2" ]; then
            echo "Usage: ./generate.sh watch [variant]"
            echo "Example: ./generate.sh watch senior-pm"
            exit 1
        fi

        case $2 in
            "senior-pm")
                echo "Watching cv_senior_pm.typ (Ctrl+C to stop)"
                typst watch cv_senior_pm.typ
                ;;
            "superintendent")
                echo "Watching cv_superintendent.typ (Ctrl+C to stop)"
                typst watch cv_superintendent.typ
                ;;
            "estimator")
                echo "Watching cv_estimator.typ (Ctrl+C to stop)"
                typst watch cv_estimator.typ
                ;;
            "exec-summary")
                echo "Watching cv_exec_summary.typ (Ctrl+C to stop)"
                typst watch cv_exec_summary.typ
                ;;
            "standard")
                echo "Watching cv.typ (Ctrl+C to stop)"
                typst watch cv.typ
                ;;
            "letter")
                echo "Watching letter.typ (Ctrl+C to stop)"
                typst watch letter.typ
                ;;
            *)
                echo "Unknown watch target: $2"
                exit 1
                ;;
        esac
        ;;

    "help"|"--help"|"-h"|"")
        echo "CV Generation Script"
        echo ""
        echo "Usage: ./generate.sh [command]"
        echo ""
        echo "Commands:"
        echo "  senior-pm        Generate Senior PM focused CV"
        echo "  superintendent   Generate Superintendent focused CV"
        echo "  estimator        Generate Estimator/Preconstruction CV"
        echo "  exec-summary     Generate one-page executive summary"
        echo "  standard         Generate standard CV (cv.typ)"
        echo "  letter           Generate cover letter"
        echo "  all              Generate all variants"
        echo "  clean            Remove all compiled PDFs"
        echo "  watch [variant]  Watch and auto-compile on changes"
        echo "  help             Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./generate.sh senior-pm       # Compile senior PM CV"
        echo "  ./generate.sh all             # Compile everything"
        echo "  ./generate.sh watch senior-pm # Auto-compile on changes"
        echo ""
        echo "CV Variants:"
        echo "  • cv_senior_pm.typ        - Senior PM emphasis"
        echo "  • cv_superintendent.typ   - Field operations emphasis"
        echo "  • cv_estimator.typ        - Preconstruction emphasis"
        echo "  • cv_exec_summary.typ     - One-page summary"
        echo "  • cv.typ                  - Standard full CV"
        echo ""
        ;;

    *)
        echo "Unknown command: $1"
        echo "Run './generate.sh help' for usage information"
        exit 1
        ;;
esac
