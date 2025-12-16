import streamlit as st
import requests

st.title("GitAudit by Talentio")

st.subheader("Repository Details")
col1, col2 = st.columns(2)
with col1:
    username = st.text_input("GitHub Username", placeholder="e.g., mohammedsonu")
with col2:
    repo = st.text_input("Repository Name", placeholder="TalentioDashboard")

st.subheader("Files to Check")

if 'file_names' not in st.session_state:
    st.session_state.file_names = ['']

def add_file():
    st.session_state.file_names.append('')

def remove_file(index):
    if len(st.session_state.file_names) > 1:
        st.session_state.file_names.pop(index)

for i, file_name in enumerate(st.session_state.file_names):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.session_state.file_names[i] = st.text_input(
            f"File {i+1}", 
            value=file_name, 
            key=f"file_{i}",
            placeholder="e.g., README.md"
        )
    with col2:
        st.write("")
        st.write("")
        if st.button("❌", key=f"remove_{i}"):
            remove_file(i)
            st.rerun()

if st.button("➕ Add File", use_container_width=True):
    add_file()
    st.rerun()

st.divider()

if st.button("🔍 Check Repository", type="primary", use_container_width=True):
    if not username or not repo:
        st.error("Please enter both username and repository name")
    else:
        files_to_check = [f for f in st.session_state.file_names if f.strip()]
        
        if not files_to_check:
            st.error("Please enter at least one file name")
        else:
            with st.spinner("Checking repository..."):
                api_url = f"https://api.github.com/repos/{username}/{repo}"
                response = requests.get(api_url)
                
                if response.status_code != 200:
                    st.error(f"❌ Repository does not exist or is not accessible: {username}/{repo}")
                else:
                    st.success(f"✅ Repository exists: {username}/{repo}")
                    
                    contents_url = f"https://api.github.com/repos/{username}/{repo}/contents"
                    contents_response = requests.get(contents_url)
                    
                    if contents_response.status_code != 200:
                        st.error("Could not retrieve repository contents")
                    else:
                        files = contents_response.json()
                        repo_files = [item['name'] for item in files if item['type'] == 'file']
                        
                        existing_files = [f for f in files_to_check if f in repo_files]
                        missing_files = [f for f in files_to_check if f not in repo_files]
                        
                        st.subheader("📊 Status Summary")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Files Checked", len(files_to_check))
                        with col2:
                            st.metric("Files Found", len(existing_files))
                        with col3:
                            st.metric("Files Missing", len(missing_files))
                        
                        if existing_files:
                            st.subheader("✅ Files Found")
                            for file in existing_files:
                                st.success(f"✓ {file}")
                        
                        if missing_files:
                            st.subheader("❌ Files Missing")
                            for file in missing_files:
                                st.error(f"✗ {file}")
                        
                        if len(existing_files) == len(files_to_check):
                            st.balloons()
                            st.success("🎉 All files exist in the repository!")