#!/usr/bin/env python3
"""
Demo script for Medical Discharge Summary Assistant
Demonstrates the core functionality without the Streamlit UI
"""

import sys
import json
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from app import MedicalRAGSystem, AutoGenMedicalAgent
    import torch
    import chromadb
    from pymongo import MongoClient
    from transformers import AutoTokenizer, AutoModel
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

def demo_rag_system():
    """Demonstrate RAG system functionality"""
    print("🔍 Testing RAG System...")
    print("-" * 40)
    
    try:
        # Initialize RAG system
        rag_system = MedicalRAGSystem()
        print("✅ RAG system initialized successfully")
        
        # Test patient search
        test_unit_no = "89330709"  # From your main.ipynb
        print(f"\n🔍 Searching for patient with unit number: {test_unit_no}")
        
        patient = rag_system.get_patient_by_unit_no(test_unit_no)
        if patient:
            print(f"✅ Found patient: {patient.get('name', 'Unknown')}")
            print(f"   Unit No: {patient.get('unit no', 'N/A')}")
            print(f"   DOB: {patient.get('date of birth', 'N/A')}")
            print(f"   Service: {patient.get('service', 'N/A')}")
        else:
            print("❌ Patient not found")
            return False
        
        # Test embedding generation
        print(f"\n🧠 Testing embedding generation...")
        patient_text = rag_system.format_patient_fields(patient)
        embedding = rag_system.embed_text(patient_text[:100])  # Use first 100 chars for demo
        print(f"✅ Generated embedding with {len(embedding)} dimensions")
        
        # Test similar cases search
        print(f"\n🔍 Testing similar cases search...")
        similar_cases = rag_system.search_similar_cases(patient_text[:200], n_results=2)
        if similar_cases:
            print(f"✅ Found {len(similar_cases)} similar cases")
            for i, case in enumerate(similar_cases):
                print(f"   Case {i+1}: Similarity = {case['similarity']:.2%}")
                print(f"   Patient: {case['metadata'].get('name', 'Unknown')}")
        else:
            print("❌ No similar cases found")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG system test failed: {str(e)}")
        return False

def demo_autogen_agent():
    """Demonstrate AutoGen agent functionality"""
    print("\n🤖 Testing AutoGen Agent...")
    print("-" * 40)
    
    try:
        # Initialize RAG system first
        rag_system = MedicalRAGSystem()
        
        # Initialize AutoGen agent
        autogen_agent = AutoGenMedicalAgent(rag_system)
        print("✅ AutoGen agent initialized successfully")
        
        # Test conversation
        test_message = "Hello, I need help generating a discharge summary for a patient with coronary artery disease."
        print(f"\n💬 Testing conversation...")
        print(f"Doctor: {test_message}")
        
        response = autogen_agent.chat_with_doctor(test_message)
        print(f"AI Assistant: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ AutoGen agent test failed: {str(e)}")
        return False

def demo_discharge_summary():
    """Demonstrate discharge summary generation"""
    print("\n📝 Testing Discharge Summary Generation...")
    print("-" * 40)
    
    try:
        # Initialize RAG system
        rag_system = MedicalRAGSystem()
        
        # Get test patient
        test_unit_no = "89330709"
        patient = rag_system.get_patient_by_unit_no(test_unit_no)
        
        if not patient:
            print("❌ Test patient not found")
            return False
        
        print(f"✅ Found test patient: {patient.get('name', 'Unknown')}")
        
        # Format patient data
        patient_text = rag_system.format_patient_fields(patient)
        print(f"✅ Formatted patient data ({len(patient_text)} characters)")
        
        # Generate discharge summary
        print(f"\n📝 Generating discharge summary...")
        print("⚠️ This may take a few minutes...")
        
        summary = rag_system.generate_discharge_summary(patient_text)
        
        if summary and not summary.startswith("❌"):
            print("✅ Discharge summary generated successfully")
            print(f"\n📄 Summary Preview (first 500 characters):")
            print("-" * 50)
            print(summary[:500] + "..." if len(summary) > 500 else summary)
            print("-" * 50)
            
            # Save summary to file
            with open("demo_summary.txt", "w") as f:
                f.write(summary)
            print(f"\n💾 Full summary saved to: demo_summary.txt")
            
            return True
        else:
            print(f"❌ Failed to generate summary: {summary}")
            return False
            
    except Exception as e:
        print(f"❌ Discharge summary test failed: {str(e)}")
        return False

def check_system_requirements():
    """Check if all system requirements are met"""
    print("🔍 Checking System Requirements...")
    print("-" * 40)
    
    requirements_met = True
    
    # Check Python packages
    packages = ["torch", "chromadb", "pymongo", "transformers", "autogen", "requests"]
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            requirements_met = False
    
    # Check Ollama connection
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama service")
        else:
            print("❌ Ollama service (not responding)")
            requirements_met = False
    except:
        print("❌ Ollama service (not running)")
        requirements_met = False
    
    # Check directories
    required_dirs = ["vector_db", "data", "embeddings", "processed"]
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/")
            requirements_met = False
    
    return requirements_met

def main():
    """Main demo function"""
    print("🏥 Medical Discharge Summary Assistant - Demo")
    print("=" * 60)
    
    # Check system requirements
    if not check_system_requirements():
        print("\n❌ System requirements not met. Please run setup.py first.")
        return 1
    
    print("\n✅ All system requirements met!")
    
    # Run demos
    demos = [
        ("RAG System", demo_rag_system),
        ("AutoGen Agent", demo_autogen_agent),
        ("Discharge Summary", demo_discharge_summary)
    ]
    
    results = {}
    for demo_name, demo_func in demos:
        print(f"\n{'='*60}")
        print(f"🧪 Running {demo_name} Demo")
        print('='*60)
        
        try:
            results[demo_name] = demo_func()
        except Exception as e:
            print(f"❌ {demo_name} demo crashed: {str(e)}")
            results[demo_name] = False
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Demo Results Summary")
    print('='*60)
    
    for demo_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{demo_name:20} {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} demos passed")
    
    if passed == total:
        print("\n🎉 All demos passed! The system is working correctly.")
        print("You can now run the full application with: streamlit run app.py")
    else:
        print(f"\n⚠️ {total - passed} demos failed. Please check the errors above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

